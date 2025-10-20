from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .provider import HolidayProvider


@dataclass
class WorkingDayCalendar:
    provider: HolidayProvider
    timezone: ZoneInfo = ZoneInfo("Asia/Shanghai")

    def _to_local_date(self, d_or_dt: date | datetime) -> date:
        if isinstance(d_or_dt, datetime):
            if d_or_dt.tzinfo is None:
                # Treat naive datetime as UTC then convert to the target timezone
                d_or_dt = d_or_dt.replace(tzinfo=ZoneInfo("UTC"))
            local_dt = d_or_dt.astimezone(self.timezone)
            return local_dt.date()
        return d_or_dt

    def is_working_day(self, d_or_dt: date | datetime) -> bool:
        d = self._to_local_date(d_or_dt)
        if self.provider.is_adjusted_workday(d):
            return True
        if self.provider.is_public_holiday(d):
            return False
        # 0=Mon .. 6=Sun
        if d.weekday() in (5, 6):
            return False
        return True

    def is_first_working_day_of_week(self, d_or_dt: date | datetime) -> bool:
        d = self._to_local_date(d_or_dt)
        # Sunday as week start
        # weekday(): Mon=0..Sun=6; index within Sunday-start week:
        days_since_sunday = (d.weekday() + 1) % 7
        week_start = d - timedelta(days=days_since_sunday)  # Sunday
        for i in range(7):
            cur = week_start + timedelta(days=i)
            if self.is_working_day(cur):
                return cur == d
        return False
