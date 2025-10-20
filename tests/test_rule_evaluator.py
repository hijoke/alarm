import json
from datetime import date

from holiday import CNHolidayProvider, WorkingDayCalendar, RuleEvaluator
from holiday.rules import And, Predicate


def test_rule_ast_serialization_and_evaluation():
    provider = CNHolidayProvider()
    evaluator = RuleEvaluator(provider)

    # Rule: working day AND first working day of the week
    rule = And([Predicate("isWorkingDay"), Predicate("isFirstWorkingDayOfWeek")])

    # Monday 2024-03-11 should be the first working day of the week (Sunday start)
    d = date(2024, 3, 11)

    # Evaluate from object
    assert evaluator.evaluate(rule.to_dict(), d) is True

    # Evaluate from JSON serialization
    s = json.dumps(rule.to_dict())
    assert evaluator.evaluate(s, d) is True


def test_or_combination_and_negative_case():
    provider = CNHolidayProvider()
    evaluator = RuleEvaluator(provider)

    # not (working day AND first working day of week) on a holiday date
    rule = {
        "type": "NOT",
        "child": {
            "type": "AND",
            "children": [
                {"type": "PREDICATE", "name": "isWorkingDay"},
                {"type": "PREDICATE", "name": "isFirstWorkingDayOfWeek"}
            ]
        }
    }

    d_holiday = date(2024, 2, 13)  # within Spring Festival long holiday week
    assert evaluator.evaluate(rule, d_holiday) is True


def test_first_working_day_after_adjusted_sunday():
    provider = CNHolidayProvider()
    evaluator = RuleEvaluator(provider)

    # isFirstWorkingDayOfWeek should be true on adjusted working Sunday 2024-02-18
    rule = {"type": "PREDICATE", "name": "isFirstWorkingDayOfWeek"}

    d = date(2024, 2, 18)
    assert evaluator.evaluate(rule, d) is True
