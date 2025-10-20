from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol, runtime_checkable

from .calendar import WorkingDayCalendar


@runtime_checkable
class Evaluatable(Protocol):
    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:  # pragma: no cover - Protocol signature
        ...


class Expression:
    def to_dict(self) -> Dict[str, Any]:  # pragma: no cover - overridden in subclasses
        raise NotImplementedError

    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:  # pragma: no cover - overridden in subclasses
        raise NotImplementedError

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Expression":
        t = d.get("type")
        if t == "AND":
            return And([Expression.from_dict(c) for c in d.get("children", [])])
        if t == "OR":
            return Or([Expression.from_dict(c) for c in d.get("children", [])])
        if t == "NOT":
            return Not(Expression.from_dict(d.get("child")))
        if t == "PREDICATE":
            return Predicate(d.get("name"))
        raise ValueError(f"Unknown expression type: {t}")


@dataclass
class And(Expression):
    children: List[Expression] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "AND", "children": [c.to_dict() for c in self.children]}

    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:
        return all(c.evaluate(calendar, subject) for c in self.children)


@dataclass
class Or(Expression):
    children: List[Expression] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "OR", "children": [c.to_dict() for c in self.children]}

    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:
        return any(c.evaluate(calendar, subject) for c in self.children)


@dataclass
class Not(Expression):
    child: Expression

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "NOT", "child": self.child.to_dict()}

    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:
        return not self.child.evaluate(calendar, subject)


@dataclass
class Predicate(Expression):
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"type": "PREDICATE", "name": self.name}

    def evaluate(self, calendar: WorkingDayCalendar, subject: Any) -> bool:
        if self.name == "isWorkingDay":
            return calendar.is_working_day(subject)
        if self.name == "isFirstWorkingDayOfWeek":
            return calendar.is_first_working_day_of_week(subject)
        raise ValueError(f"Unknown predicate: {self.name}")
