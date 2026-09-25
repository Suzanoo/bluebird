"""F1 semantic planning. No web framework, workbook coordinates or Excel imports.

Distribution follows PS distribution_workbook.distribute at 89a6b80; pure
curve and auto-rule modules are reused verbatim. F0 normalization is shared.
"""
from dataclasses import dataclass
from datetime import timedelta
import math

from .distribution.auto import decide_distribution, load_rules
from .distribution.curves import get_distribution

WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
DISTRIBUTIONS = ('auto', 'flat', 'front', 'back', 'bell')


class InputError(ValueError):
    """Safe, bounded user-facing validation error, never arbitrary exception text."""


@dataclass(frozen=True)
class Settings:
    method: str
    cutoff: str = 'Friday'
    distribution: str = 'auto'

    def __post_init__(self):
        if self.method not in ('Equal', 'Duration'):
            raise InputError('Select Equal or Duration explicitly.')
        if self.cutoff not in WEEKDAYS:
            raise InputError('Select a valid weekly cutoff day.')
        if self.distribution not in DISTRIBUTIONS:
            raise InputError('Select auto, flat, front, back or bell distribution.')


def weight_bases(schedule, method):
    Settings(method)
    values, invalid = [], []
    for a in schedule.activities:
        if a.milestone:
            values.append(0.0)
        elif method == 'Equal':
            values.append(1.0)
        elif a.duration_hours is None or not math.isfinite(a.duration_hours) or a.duration_hours <= 0:
            invalid.append(a.source_id[:60])
        else:
            values.append(a.duration_hours)
    if invalid:
        raise InputError('Duration requires positive source working hours. Check Activity IDs: '
                         + ', '.join(invalid[:8]) + (' …' if len(invalid) > 8 else ''))
    if not math.isfinite(sum(values)) or sum(values) <= 0:
        raise InputError('At least one ordinary activity with positive weight is required.')
    return values


def reporting_weeks(schedule, cutoff):
    dated = [a for a in schedule.activities if a.start and a.finish]
    if not dated:
        raise InputError('No usable activity date range was found.')
    first, last = min(a.start for a in dated), max(a.finish for a in dated)
    end = first + timedelta(days=(WEEKDAYS.index(cutoff) - first.weekday()) % 7)
    result = []
    while end - timedelta(days=6) <= last:
        result.append(end)
        if len(result) > 260:
            raise InputError('This version supports at most 260 reporting weeks.')
        end += timedelta(days=7)
    return result


def distribute(activity, periods, method):
    if not activity.start or not activity.finish:
        return [None] * len(periods)
    active = []
    for i, end in enumerate(periods):
        days = (min(activity.finish, end) - max(activity.start, end - timedelta(days=6))).days + 1
        if days > 0:
            active.append((i, days))
    result = [None] * len(periods)
    if not active:
        return result
    curve = get_distribution(method).generator(len(active))
    combined = [w * days / 7 for w, (_, days) in zip(curve, active)]
    total = sum(combined)
    normalized = [v / total for v in combined]
    normalized[-1] = max(0.0, 1.0 - sum(normalized[:-1])) if len(normalized) > 1 else 1.0
    for (i, _), value in zip(active, normalized):
        result[i] = value
    return result


def prepare(schedule, settings):
    weights = weight_bases(schedule, settings.method)
    periods = reporting_weeks(schedule, settings.cutoff)
    wbs = {w.key: w for w in schedule.wbs}
    rules = load_rules()
    plans, methods, warnings = [], [], []
    for a in schedule.activities:
        method = settings.distribution
        if method == 'auto':
            node = wbs.get(a.wbs)
            # PS's WBS input is the displayed code, not invented concatenated names.
            method = decide_distribution(activity_code=a.source_id,
                wbs=node.code if node else '', activity_name=a.name, rules=rules).distribution
        plans.append(distribute(a, periods, method))
        methods.append(method)
        if not a.start or not a.finish:
            warnings.append(f'{a.source_id}: Plan allocation skipped (missing dates).')
    return weights, periods, plans, methods, warnings
