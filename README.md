Holiday Provider and Boolean Rule Engine

Overview
- A simple, self-contained Python package that provides:
  - A HolidayProvider abstraction with a default CNHolidayProvider that reads bundled Chinese public holidays and adjusted workdays (调休) from JSON files in assets/raw.
  - A WorkingDayCalendar utility that determines working days, honoring:
    - Sunday as the start of the week
    - Public holidays
    - Adjusted workdays that fall on weekends
  - A small boolean rule-expression AST supporting AND/OR/NOT nodes and two built-in predicates:
    - isWorkingDay
    - isFirstWorkingDayOfWeek
  - A RuleEvaluator to evaluate rules against dates with timezone awareness.

Getting Started
- No external dependencies are required beyond Python 3.10+ (uses zoneinfo).
- The package is located in the holiday/ directory with unit tests under tests/.

Key Concepts
- HolidayProvider: Returns whether a given local date is a public holiday or an adjusted workday.
- WorkingDayCalendar: Provides is_working_day and is_first_working_day_of_week utilities driven by a HolidayProvider.
- Rule AST: You can build expressions like {"type":"AND","children":[{"type":"PREDICATE","name":"isWorkingDay"}, {"type":"NOT","child":{"type":"PREDICATE","name":"isFirstWorkingDayOfWeek"}}]}.
- RuleEvaluator: Evaluate a rule against a date/datetime in a specific timezone (default Asia/Shanghai). The local date derived from the timezone is used when checking holidays and working days.

Data Format (assets/raw/cn_holidays_2024_2026.json)
- This JSON covers 2024-2026 with public holidays and adjusted workdays.
- Example structure:
{
  "country": "CN",
  "years": {
    "2024": {
      "public_holidays": ["2024-01-01", "2024-02-10", "2024-02-11", ...],
      "adjusted_workdays": ["2024-02-04", "2024-02-18", ...]
    },
    "2025": {
      "public_holidays": ["2025-01-01"],
      "adjusted_workdays": []
    },
    "2026": {
      "public_holidays": ["2026-01-01"],
      "adjusted_workdays": []
    }
  }
}

Updating Holiday Data
- Edit assets/raw/cn_holidays_2024_2026.json directly, or use the helper script tools/update_cn_holidays.py to merge new dates.
- After updating, run tests to ensure behavior remains correct.

Predicates
- isWorkingDay: True if the local date is a working day in CN (Mon–Fri excluding public holidays, plus any adjusted workdays even if they fall on Sat/Sun).
- isFirstWorkingDayOfWeek: Uses Sunday as the start of the week. Returns true if the local date is the first working day in that week (considering holidays and adjusted workdays). If a week has no working day (e.g., a full holiday week), the predicate is false for all days in that week.

Examples
- JSON rule for “working day AND first working day of the week”:
{"type": "AND", "children": [
  {"type": "PREDICATE", "name": "isWorkingDay"},
  {"type": "PREDICATE", "name": "isFirstWorkingDayOfWeek"}
]}

License
- MIT
