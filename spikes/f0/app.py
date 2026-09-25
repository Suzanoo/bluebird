"""F0 same-origin HTTP adapter. No persistence or change to workbook semantics."""
from pathlib import Path
from threading import Lock
from time import monotonic
from xml.parsers.expat import ExpatError
from xml.etree.ElementTree import ParseError

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.concurrency import run_in_threadpool
from starlette.requests import ClientDisconnect
from openpyxl.worksheet._writer import ALL_TEMP_FILES

from run import convert
from engine.service import convert as convert_f1
from engine.domain import Settings, InputError

MAX_BYTES = 4_000_000
TARGET_SECONDS = 60
XLSX_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# Nonblocking admission, not a work queue. All renders in this process use this lock.
_conversion_lock = Lock()
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


def error(status, code, message):
    return JSONResponse({'error': {'code': code, 'message': message}}, status_code=status,
                        headers={'Cache-Control': 'no-store'})


def generate(raw, method, settings=None):
    if not _conversion_lock.acquire(blocking=False):
        return error(503, 'busy', 'Converter is busy. Please try again shortly.')
    before = set(ALL_TEMP_FILES)
    started = monotonic()
    try:
        try:
            data, info = (convert_f1(raw, method, settings.cutoff, settings.distribution)
                          if settings else convert(raw, method))
            if monotonic() - started > TARGET_SECONDS:
                return error(504, 'timeout', 'Conversion exceeded the 60-second runtime target.')
            if len(data) > MAX_BYTES:
                return error(413, 'output_too_large', 'Workbook exceeds the current 4 MB limit.')
            return Response(data, media_type=XLSX_TYPE, headers={
                'Content-Disposition': 'attachment; filename="progress.xlsx"' if settings else 'attachment; filename="progress-f0.xlsx"',
                'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff',
                'X-Bluebird-Warnings': str(info.get('warnings', 0)),
            })
        except (ExpatError, ParseError):
            return error(400, 'invalid_xml', 'The file is not valid XML.')
        except InputError as exc:
            return error(422, 'invalid_schedule', str(exc))
        except ValueError as exc:
            if str(exc) == 'F0 output exceeds 4 MB response cap':
                return error(413, 'output_too_large', 'Workbook exceeds the 4 MB proof limit.')
            return error(422, 'unsupported_input',
                         'Unsupported schedule. Check one-project XML, unique activity IDs, hierarchy and valid dates.' if settings else
                         'Schedule or weighting is unsupported by this proof. Duration requires usable source durations.')
        except Exception:
            return error(500, 'conversion_failed', 'Workbook conversion failed.')
    finally:
        # openpyxl 3.1.5 tracks its worksheet scratch paths. Normal save removes
        # them; on a catchable failure remove only paths added by this serialized
        # conversion. Never sweep /tmp or touch another request's files.
        try:
            for filename in set(ALL_TEMP_FILES) - before:
                try:
                    Path(filename).unlink(missing_ok=True)
                except OSError:
                    # Leave registered for openpyxl's process-exit cleanup.
                    continue
                if filename in ALL_TEMP_FILES:
                    ALL_TEMP_FILES.remove(filename)
        finally:
            _conversion_lock.release()


async def handle_upload(request: Request, settings=None):
    methods = request.query_params.getlist('method')
    if len(methods) != 1 or methods[0] not in ('Equal', 'Duration'):
        return error(422, 'invalid_method', 'Select Equal or Duration explicitly.')
    if request.headers.get('content-type', '').split(';', 1)[0].strip().lower() not in ('application/xml', 'text/xml'):
        return error(415, 'invalid_content_type', 'Upload XML using application/xml.')
    if request.headers.get('content-encoding', 'identity').lower() != 'identity':
        return error(415, 'unsupported_encoding', 'Compressed uploads are not supported.')
    length = request.headers.get('content-length')
    declared_oversize = False
    if length is not None:
        if not length.isascii() or not length.isdecimal():
            return error(400, 'invalid_length', 'Invalid upload length.')
        # Avoid converting an unbounded integer string.
        declared_oversize = len(length) > 10 or int(length) > MAX_BYTES
        # Read only up to the bounded stream limit before responding: local
        # Services can replace an early response during upload with proxy 500.
    raw = bytearray()
    try:
        async for chunk in request.stream():
            if len(raw) + len(chunk) > MAX_BYTES:
                return error(413, 'upload_too_large', 'XML must be at most 4 MB.')
            raw.extend(chunk)
    except ClientDisconnect:
        return error(400, 'upload_interrupted', 'Upload was interrupted.')
    if declared_oversize:
        return error(413, 'upload_too_large', 'XML must be at most 4 MB.')
    if not raw:
        return error(400, 'missing_upload', 'Select a non-empty XML file.')
    if length is not None and len(raw) != int(length):
        return error(400, 'invalid_length', 'Upload length does not match the body.')
    # A thread keeps HTTP handling responsive; it is not a background job.
    # Disconnect/timeout does not forcibly cancel CPU work. The platform duration
    # and client deadline are separate; generate rejects results finished late.
    return await run_in_threadpool(generate, bytes(raw), methods[0], settings)


@app.post('/api/f0/convert')
async def convert_xml(request: Request):
    return await handle_upload(request)


@app.post('/api/progress/convert')
async def create_workbook(request: Request):
    for key in ('method', 'cutoff', 'distribution'):
        if len(request.query_params.getlist(key)) > 1:
            return error(422, 'invalid_config', 'Each setting must be supplied once.')
    try:
        settings = Settings(request.query_params.get('method', ''),
                            request.query_params.get('cutoff', 'Friday'),
                            request.query_params.get('distribution', 'auto'))
    except InputError as exc:
        return error(422, 'invalid_config', str(exc))
    return await handle_upload(request, settings)
