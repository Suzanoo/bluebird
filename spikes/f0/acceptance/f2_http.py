"""Synthetic F2 HTTP acceptance against a separately started local/Preview URL.

No private XML, workbook persistence, authentication, Git or deployment.
Run from repository root: python spikes/f0/acceptance/f2_http.py URL
"""
from io import BytesIO
import json
from pathlib import Path
import sys
from time import monotonic
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from test_f2 import amount_xml, selected


def check(base):
    def post(path, raw, query=''):
        request = Request(base.rstrip('/')+'/api/progress/'+path+'?'+query,
                          data=raw, headers={'Content-Type': 'application/xml'})
        try:
            response = urlopen(request, timeout=65)
        except HTTPError as exc:
            response = exc
        with response:
            return response.status, response.headers, response.read()

    for source in ('msp', 'p6'):
        raw = amount_xml(source)
        code, _, data = post('amount-preview', raw)
        assert code == 200 and len(json.loads(data)['fields']) == 2
        code, _, data = post('amount-preview', raw, 'amount_field='+selected(source))
        payload = json.loads(data)
        assert code == 200 and payload['preview']['valid']
        assert payload['preview']['ordinary_total'] == '400'
        query = 'method=Amount&amount_field='+selected(source)+'&source_hash='+payload['source_hash']
        start = monotonic()
        code, headers, data = post('convert', raw, query)
        elapsed = monotonic()-start
        assert code == 200 and 'spreadsheetml.sheet' in headers['Content-Type']
        assert 'progress.xlsx' in headers['Content-Disposition']
        with ZipFile(BytesIO(data)) as z: assert z.testzip() is None
        print(f'{source}: discover/preview/convert PASS; XML {len(raw)} bytes; XLSX {len(data)} bytes; convert {elapsed:.3f}s')
        bad = amount_xml(source, ('100','300','0','bad'))
        code, _, data = post('convert', bad, 'method=Amount&amount_field='+selected(source))
        assert code == 422 and '4 (Work 4)' in json.loads(data)['error']['message']
        code, _, data = post('convert', raw, query.replace(payload['source_hash'], 'changed'))
        assert code == 422 and json.loads(data)['error']['code'] == 'stale_preview'
        print(f'{source}: invalid milestone and stale preview PASS')


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit('Usage: f2_http.py http://127.0.0.1:3000')
    check(sys.argv[1])
