"""Source adapter -> canonical model -> domain -> workbook renderer."""
from dataclasses import asdict
from .amount import preview_amounts
from model import parse_xml, normalize
from .domain import Settings, prepare
from .workbook import render


def convert(raw, method, cutoff='Friday', distribution='auto', amount_field=None):
    settings = Settings(method, cutoff, distribution, amount_field)
    schedule = normalize(parse_xml(raw), raw, production=True)
    selection = preview_amounts(schedule, amount_field).require_valid() if method == 'Amount' else None
    prepared = prepare(schedule, settings, selection)
    return render(schedule, settings, prepared, selection), {'warnings': len(prepared[-1])}


def inspect_amount(raw, selected=None):
    schedule = normalize(parse_xml(raw), raw, production=True)
    return {'source_hash': schedule.source_hash, 'source_system': schedule.source_system,
            'fields': [asdict(f) for f in schedule.amount_fields],
            'preview': preview_amounts(schedule, selected).payload() if selected else None}
