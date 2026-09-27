"""MS-2 Decimal preview/validation, adapted for Bluebird Policy A.

Source-neutral; no XML, framework or workbook coordinates. Activity money and
creation progress basis are separate. All assignments are atomic after validation.
"""
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, localcontext
import math
import re

from model import AmountField
from .domain import InputError

NUMBER = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?')


@dataclass(frozen=True)
class AmountRow:
    key: str
    activity_id: str
    name: str
    milestone: bool
    raw_values: tuple[str | None, ...]
    value: Decimal | None
    status: str


@dataclass(frozen=True)
class AmountPreview:
    field: AmountField
    rows: tuple[AmountRow, ...]
    total: Decimal
    positive_count: int
    zero_count: int
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def valid(self): return not self.errors

    @property
    def bases(self):
        if not self.valid: raise InputError('Amount selection has validation errors.')
        return [0.0 if row.milestone else float(row.value) for row in self.rows]

    def require_valid(self):
        if self.errors:
            raise InputError('Invalid XML Amount: ' + ' | '.join(self.errors[:8])
                             + (' | More errors; inspect the Amount preview.' if len(self.errors) > 8 else ''))
        return self

    def payload(self):
        return {'field': asdict(self.field), 'valid': self.valid,
            'ordinary_count': sum(not row.milestone for row in self.rows),
            'milestone_count': sum(row.milestone for row in self.rows),
            'positive_count': self.positive_count, 'zero_count': self.zero_count,
            'ordinary_total': str(self.total), 'errors': self.errors, 'warnings': self.warnings,
            'rows': [{**asdict(row), 'value': None if row.value is None else str(row.value)}
                     for row in self.rows]}


def preview_amounts(schedule, selected):
    if not selected:
        raise InputError('Select an XML Amount field explicitly.')
    matches = [f for f in schedule.amount_fields if f.identity == selected]
    if len(matches) != 1:
        raise InputError('Selected Amount field is missing, not numeric or ambiguously declared: ' + selected[:100])
    field = matches[0]
    rows, errors, warnings, ordinary = [], [], [], []
    positive = zero = 0
    for a in schedule.activities:
        raw_values = tuple(v for k, v in a.amount_field_values if k == selected)
        raw = raw_values[0] if len(raw_values) == 1 else None
        amount, issue, status = None, None, 'OK'
        if len(raw_values) > 1:
            issue = 'duplicate/ambiguous Amount values'
        elif raw is None or not raw.strip():
            if a.milestone:
                status = 'Missing milestone Amount retained blank; zero Progress Weight'
            else:
                issue = 'missing/blank Amount'
        else:
            try:
                amount = Decimal(raw.strip())
                if not amount.is_finite(): issue = 'non-finite Amount'
                elif not NUMBER.fullmatch(raw.strip()): issue = 'non-numeric Amount'
                elif amount < 0: issue = 'negative Amount'
                elif not math.isfinite(float(amount)) or (amount > 0 and float(amount) == 0):
                    issue = 'Amount outside supported workbook numeric range'
            except (InvalidOperation, ValueError, OverflowError):
                issue = 'non-numeric Amount'
        context = f'{a.source_id[:60]} ({a.name[:80]}) — {field.name[:80]} [{field.identity[:100]}]'
        if issue:
            errors.append(context + ': ' + issue)
            amount, status = None, issue
        elif a.milestone:
            if amount is None: warnings.append(context + ': ' + status)
            else: status = 'Milestone Amount retained; zero Progress Weight'
        else:
            ordinary.append(amount)
            positive += amount > 0
            zero += amount == 0
            if amount == 0: status = 'Zero Amount'
        rows.append(AmountRow(a.key, a.source_id, a.name, a.milestone, raw_values, amount, status))
    with localcontext() as ctx:
        # Exact sum as MS-2; only accepted finite workbook-range numbers enter it.
        ctx.prec = max(28, max((v.adjusted() for v in ordinary if v), default=0)
            - min((v.as_tuple().exponent for v in ordinary if v), default=0)
            + len(str(len(ordinary))) + 4)
        total = sum((v for v in ordinary if v), Decimal(0))
    if not errors and (total <= 0 or not math.isfinite(float(total))
                       or not math.isfinite(sum(float(v) for v in ordinary))):
        errors.append(f'{field.name[:80]} [{field.identity[:100]}]: ordinary Amount total must be positive and within supported workbook numeric range.')
    return AmountPreview(field, tuple(rows), total, positive, zero, tuple(errors), tuple(warnings))
