"""Source adapter -> canonical model -> domain -> workbook renderer."""
from model import parse_xml, normalize
from .domain import Settings, prepare
from .workbook import render


def convert(raw, method, cutoff='Friday', distribution='auto'):
    settings = Settings(method, cutoff, distribution)
    schedule = normalize(parse_xml(raw), raw, production=True)
    prepared = prepare(schedule, settings)
    return render(schedule, settings, prepared), {'warnings': len(prepared[-1])}
