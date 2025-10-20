from datetime import date, datetime
from zoneinfo import ZoneInfo

from holiday import CNHolidayProvider, WorkingDayCalendar


def test_regular_weekday_is_working_day():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    assert cal.is_working_day(date(2024, 3, 20)) is True  # Wednesday


def test_weekend_is_not_working_day():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    assert cal.is_working_day(date(2024, 3, 16)) is False  # Saturday
    assert cal.is_working_day(date(2024, 3, 17)) is False  # Sunday


def test_adjusted_weekend_is_working_day():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    assert cal.is_working_day(date(2024, 4, 7)) is True  # Sunday adjusted workday


def test_public_holiday_on_weekday_is_not_working_day():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    assert cal.is_working_day(date(2024, 5, 1)) is False  # Labor Day holiday


def test_first_working_day_of_week_after_full_holiday_week():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    # Entire week 2024-02-11..2024-02-17 is holidays
    assert cal.is_first_working_day_of_week(date(2024, 2, 12)) is False
    # Next week starts on Sunday 2024-02-18 which is an adjusted workday
    assert cal.is_first_working_day_of_week(date(2024, 2, 18)) is True
    assert cal.is_first_working_day_of_week(date(2024, 2, 19)) is False


def test_first_working_day_of_normal_week_sunday_start():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)
    # Week starting on Sunday 2024-03-10 -> first working day is Monday 2024-03-11
    assert cal.is_first_working_day_of_week(date(2024, 3, 10)) is False  # Sunday
    assert cal.is_first_working_day_of_week(date(2024, 3, 11)) is True   # Monday


def test_timezone_awareness_default_asia_shanghai():
    provider = CNHolidayProvider()
    cal = WorkingDayCalendar(provider)  # default Asia/Shanghai
    # 2024-02-10 17:00 UTC => 2024-02-11 01:00 CST (holiday)
    dt_utc = datetime(2024, 2, 10, 17, 0, 0)  # naive treated as UTC
    assert cal.is_working_day(dt_utc) is False


def test_timezone_difference_changes_result():
    provider = CNHolidayProvider()
    # In Asia/Shanghai, 2024-04-07 is adjusted workday; but the same UTC moment
    # is still 2024-04-06 in America/Los_Angeles which is a holiday.
    dt_utc = datetime(2024, 4, 6, 23, 30, 0)  # naive treated as UTC

    cal_sh = WorkingDayCalendar(provider, ZoneInfo("Asia/Shanghai"))
    cal_la = WorkingDayCalendar(provider, ZoneInfo("America/Los_Angeles"))

    assert cal_sh.is_working_day(dt_utc) is True
    assert cal_la.is_working_day(dt_utc) is False
