"""Disposable F0 adapter/domain proof. No framework or spreadsheet imports."""
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
from uuid import uuid4, uuid5, UUID
import math
import re
from xml.etree import ElementTree as ET
from xml.parsers import expat

@dataclass(frozen=True)
class AmountField:
    identity: str
    name: str
    source: str
    data_type: str
    native_name: str = ''

@dataclass(frozen=True)
class Wbs:
    key: str
    source_id: str
    code: str
    name: str
    parent: str | None
    source_order: int | None = None
    sequence_number: int | None = None

@dataclass(frozen=True)
class Activity:
    key: str
    source_object_id: str | None
    source_id: str
    name: str
    wbs: str | None
    start: date | None
    finish: date | None
    duration_hours: float | None
    duration_field: str
    duration_raw: str
    calendar_id: str
    milestone: bool
    source_task_id: str = ''
    source_id_field: str = ''
    duration_format: str = ''
    source_status: str = ''
    source_type: str = ''
    start_raw: str = ''
    finish_raw: str = ''
    amount_field_values: tuple[tuple[str, str | None], ...] = ()
    source_order: int | None = None

@dataclass(frozen=True)
class Schedule:
    import_id: str
    source_hash: str
    source_system: str
    source_project: str
    wbs: tuple[Wbs, ...]
    activities: tuple[Activity, ...]
    source_project_fields: tuple[tuple[str, str], ...] = ()
    amount_fields: tuple[AmountField, ...] = ()

def value(e, name):
    n = e.find(name)
    return (n.text or '').strip() if n is not None else ''

def parse_xml(raw):
    if len(raw) > 4_000_000:
        raise ValueError('XML exceeds F0 4 MB byte limit')
    # Expat preflight catches declarations even in UTF-16; no regex-only filter.
    checker = expat.ParserCreate()
    def forbidden(*args): raise ValueError('DTD/entities are not supported')
    checker.StartDoctypeDeclHandler = forbidden
    checker.EntityDeclHandler = forbidden
    checker.ExternalEntityRefHandler = forbidden
    depth, count = 0, 0
    def start(*args):
        nonlocal depth, count
        depth += 1; count += 1
        if depth > 64 or count > 100000: raise ValueError('XML complexity limit')
    def end(*args):
        nonlocal depth
        depth -= 1
    checker.StartElementHandler = start; checker.EndElementHandler = end
    checker.Parse(raw, True)
    root = ET.fromstring(raw)
    for n in root.iter():
        n.tag = n.tag.rsplit('}', 1)[-1]
    return root

def sequence_number(raw):
    """PS SequenceNumber concept; unavailable/non-finite values fall back to encounter order."""
    try:
        return int(float(raw)) if raw else None
    except (ValueError, OverflowError):
        return None


def ordered_children(source_system, wbs, activities):
    """Order one sibling group without changing identity or activity-list indices.

    activities contains (canonical index, Activity). P6 collections have no shared
    interleaving: direct activities precede child WBS as in PS 89a6b80. MSP uses
    a shared task encounter index. MSP models lacking that metadata keep legacy group
    order (child WBS then direct activities), never inferred WBS-code sorting.
    """
    def encounter(item, fallback):
        return item.source_order if item.source_order is not None else fallback
    children = [('WBS', None, w) for w in wbs]
    tasks = [('Activity', i, a) for i, a in activities]
    if source_system == 'MSP':
        combined = children + tasks
        if all(item.source_order is not None for _, _, item in combined):
            return sorted(combined, key=lambda entry: entry[2].source_order)
        return combined
    children = [entry for _, entry in sorted(enumerate(children), key=lambda pair: (
        pair[1][2].sequence_number is None,
        pair[1][2].sequence_number if pair[1][2].sequence_number is not None
        else encounter(pair[1][2], pair[0]), encounter(pair[1][2], pair[0])))]
    tasks = [entry for _, entry in sorted(enumerate(tasks),
             key=lambda pair: encounter(pair[1][2], pair[0]))]
    return tasks + children


def normalize(root, raw, import_id=None, msp_activity_id_field=None, *, production=False):
    iid = import_id or str(uuid4())
    def key(kind, source): return str(uuid5(UUID(iid), kind + ':' + source))
    msp = root.tag == 'Project' and root.find('Tasks') is not None
    projects = [root] if msp else root.findall('Project')
    if len(projects) != 1: raise ValueError('Exactly one supported project required')
    p = projects[0]
    # MS-2 declarations own field identity/type; never infer from alias or value.
    # Reuse this traversal for monetary provenance without changing activity IDs.
    numeric_types = {'double': 'DoubleValue', 'integer': 'IntegerValue', 'cost': 'CostValue'}
    if msp:
        fields = tuple(AmountField('msp:field:' + value(e, 'FieldID'),
            value(e, 'Alias') or value(e, 'FieldName') or value(e, 'FieldID'), 'MSP',
            'Number' if value(e, 'CFType') == '5' else 'Numeric', value(e, 'FieldName'))
            for e in p.findall('ExtendedAttributes/ExtendedAttribute')
            if value(e, 'FieldID') and (value(e, 'CFType') == '5'
                or re.fullmatch(r'(?:Number|Cost)\d+', value(e, 'FieldName'))))
    else:
        fields = tuple(AmountField('p6:udf:' + value(e, 'ObjectId'),
            value(e, 'Title') or value(e, 'ObjectId'), 'P6', value(e, 'DataType'))
            for e in root.iter('UDFType') if value(e, 'ObjectId')
            and value(e, 'SubjectArea').lower() == 'activity'
            and value(e, 'DataType').lower() in numeric_types)
    eligible = {f.identity: f for f in fields}
    def amount_values(a):
        found = []
        for e in a.findall('ExtendedAttribute' if msp else 'UDF'):
            identity = ('msp:field:' + value(e, 'FieldID') if msp
                        else 'p6:udf:' + value(e, 'TypeObjectId'))
            if identity not in eligible: continue
            tag = 'Value' if msp else numeric_types[eligible[identity].data_type.lower()]
            nodes = e.findall(tag)
            # Preserve duplicates (including duplicate Value children) for validation.
            found.extend((identity, n.text or '') for n in nodes)
            if not nodes: found.append((identity, None))
        return tuple(found)
    wbs, rows = [], []
    if msp:
        # Only a declared business alias or explicitly evidenced mapping selects
        # a custom field. Text1/FieldID alone does not imply a P6 Activity ID.
        declared = {value(e, 'FieldID') for e in p.findall('ExtendedAttributes/ExtendedAttribute')
                    if value(e, 'Alias').strip().casefold() in ('activity id', 'p6 activity id')}
        if msp_activity_id_field is None:
            if len(declared) > 1: raise ValueError('Ambiguous Activity ID aliases')
            msp_activity_id_field = next(iter(declared), None)
        selected_values = set()
        stack = []
        for source_order, t in enumerate(p.findall('Tasks/Task')):
            level = int(value(t, 'OutlineLevel') or 1)
            while stack and stack[-1][0] >= level: stack.pop()
            if value(t, 'Summary') == '1':
                if value(t, 'UID') == '0': continue
                src = value(t, 'UID')
                if not src: raise ValueError('Missing summary UID')
                k = key('wbs', src)
                wbs.append(Wbs(k, src, value(t, 'WBS'), value(t, 'Name'), stack[-1][1] if stack else None, source_order))
                stack.append((level, k))
            else:
                if msp_activity_id_field:
                    found = [value(a, 'Value') for a in t.findall('ExtendedAttribute') if value(a, 'FieldID') == msp_activity_id_field]
                    if len(found) != 1 or not found[0] or found[0] in selected_values:
                        raise ValueError('Missing/duplicate explicitly mapped Activity ID')
                    sid = found[0]; selected_values.add(sid)
                else:
                    sid = value(t, 'ID')
                rows.append((t, sid, value(t, 'UID'), stack[-1][1] if stack else None, source_order))
    else:
        for source_order, w in enumerate(p.findall('WBS')):
            src, parent = value(w, 'ObjectId'), value(w, 'ParentObjectId')
            if not src: raise ValueError('Missing WBS ObjectId')
            wbs.append(Wbs(key('wbs', src), src, value(w, 'Code'), value(w, 'Name'), key('wbs', parent) if parent else None, source_order, sequence_number(value(w, 'SequenceNumber'))))
        rows = [(a, value(a, 'Id'), value(a, 'ObjectId'), key('wbs', value(a, 'WBSObjectId')) if value(a, 'WBSObjectId') else None, source_order) for source_order, a in enumerate(p.findall('Activity'))]
    if not rows or len(rows) > 2000: raise ValueError('F0 accepts 1..2000 activities')
    by_wbs = {w.key:w for w in wbs}
    if len(by_wbs) != len(wbs): raise ValueError('Duplicate WBS identity')
    for w in wbs:
        seen, node = set(), w
        while node:
            if node.key in seen: raise ValueError('WBS cycle')
            seen.add(node.key)
            if node.parent and node.parent not in by_wbs: raise ValueError('Missing WBS parent')
            node = by_wbs.get(node.parent)
    activities, seen = [], set()
    for index, (a, sid, obj, wk, source_order) in enumerate(rows):
        if wk and wk not in by_wbs: raise ValueError('Missing activity WBS')
        if not sid or not value(a, 'Name'): raise ValueError('Missing activity ID/name')
        # Source object identity preferred. Missing object ID explicitly retains None.
        identity = 'object:' + obj if obj else 'id:' + sid
        if identity in seen: raise ValueError('Ambiguous duplicate source identity')
        seen.add(identity)
        def source_date(field):
            text = value(a, field)
            if production and not text: return None
            return date.fromisoformat(text[:10])
        start = source_date('Start' if msp else 'PlannedStartDate')
        finish = source_date('Finish' if msp else 'PlannedFinishDate')
        if start and finish and finish < start: raise ValueError('Finish before start')
        field = 'Duration' if msp else 'PlannedDuration'
        dur = value(a, field)
        hours = None
        if dur:
            if msp:
                match = re.fullmatch(r'PT(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?', dur)
                if match and any(match.groups()):
                    h, m, s = (float(x or 0) for x in match.groups()); hours = h + m/60 + s/3600
            else:
                try: hours = float(dur)
                except ValueError: pass
            if hours is not None and (not math.isfinite(hours) or hours < 0): hours = None
        milestone = value(a, 'Milestone') == '1' if msp else value(a, 'Type') in ('Start Milestone', 'Finish Milestone')
        # Microsoft DurationFormat: 3/5/7/9/11 are working units. Even
        # 4/6/8/10/12 are elapsed. Estimated/percent/unknown remain unsupported.
        duration_format = value(a, 'DurationFormat') or (value(p, 'DurationFormat') if msp else '')
        # F0's format gate remains historical proof behavior. PS MS-1 production
        # policy reads the explicit ISO Duration, independent of display format.
        if not production and msp and (duration_format not in ('3','5','7','9','11') or value(a, 'Manual') == '1'):
            hours = None
        activities.append(Activity(key('activity', identity), obj or None, sid, value(a, 'Name'), wk, start, finish, hours, field, dur, value(a, 'CalendarUID' if msp else 'CalendarObjectId'), milestone, value(a, 'ID') if msp else '', ('ExtendedAttribute:' + msp_activity_id_field if msp_activity_id_field else 'ID') if msp else 'Id', duration_format, value(a, 'Status') if not msp else '', value(a, 'Type'), value(a, 'Start' if msp else 'PlannedStartDate'), value(a, 'Finish' if msp else 'PlannedFinishDate')))
    from dataclasses import replace
    activities = [replace(a, amount_field_values=amount_values(source[0]), source_order=source[4])
                  for a, source in zip(activities, rows)]
    return Schedule(iid, sha256(raw).hexdigest(), 'MSP' if msp else 'P6', value(p, 'UID' if msp else 'ObjectId') or value(p, 'Id') or value(p, 'Name'), tuple(wbs), tuple(activities), tuple((k, value(p,k)) for k in ('UID','Id','ObjectId','GUID','Name') if value(p,k)), fields)

def bases(schedule, method):
    if method not in ('Equal', 'Duration'): raise ValueError('Explicit Equal or Duration required')
    if method == 'Equal': return [1.0] * len(schedule.activities)
    result = []
    for a in schedule.activities:
        d = a.duration_hours
        if d is None or (d == 0 and not a.milestone) or (a.milestone and d != 0):
            raise ValueError('Duration unavailable/inconsistent for ' + a.source_id + '; choose Equal explicitly or correct source')
        result.append(d)
    if sum(result) <= 0: raise ValueError('Duration denominator is zero; choose Equal explicitly')
    return result

def aggregate(basis, progress):
    if len(basis) != len(progress) or sum(basis) <= 0: raise ValueError('Invalid aggregation inputs')
    return sum(b*p for b,p in zip(basis,progress))/sum(basis)

def weeks(schedule):
    first = min(a.start for a in schedule.activities)
    last = max(a.finish for a in schedule.activities)
    end = first + timedelta(days=6-first.weekday())
    out = []
    while end <= last + timedelta(days=6):
        out.append(end); end += timedelta(days=7)
    if len(out) > 260: raise ValueError('F0 limit: 260 weekly periods')
    return out

def plan_profile(activity, periods):
    # Explicit F0 calendar-day flat distribution; not a working-calendar engine.
    days = (activity.finish-activity.start).days+1
    return [max(0, (min(activity.finish,e)-max(activity.start,e-timedelta(days=6))).days+1)/days for e in periods]
