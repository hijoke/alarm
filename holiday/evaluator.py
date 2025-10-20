from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo

from .calendar import WorkingDayCalendar
from .provider import HolidayProvider
from .rules import Expression


@dataclass
class RuleEvaluator:
    provider: HolidayProvider
    timezone: ZoneInfo | None = None

    def evaluate(self, expr: Expression | Dict[str, Any] | str, subject: date | datetime) -> bool:
        if isinstance(expr, str):
            expr = Expression.from_dict(json.loads(expr))
        elif isinstance(expr, dict):
            expr = Expression.from_dict(expr)

        tz = self.timezone or ZoneInfo("Asia/Shanghai")
        calendar = WorkingDayCalendar(self.provider, tz)
        return expr.evaluate(calendar, subject)
