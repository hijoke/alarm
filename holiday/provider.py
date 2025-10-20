from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Iterable


class HolidayProvider(ABC):
    """
    Abstract provider of holiday information.

    Implementations should answer whether a date is a public holiday or an
    adjusted workday (weekend working day) for a given locale.
    """

    @abstractmethod
    def is_public_holiday(self, d: date) -> bool:
        """Return True if the local date d is a public holiday."""
        raise NotImplementedError

    @abstractmethod
    def is_adjusted_workday(self, d: date) -> bool:
        """
        Return True if the local date d is an adjusted workday (调休),
        typically a weekend day designated as a working day.
        """
        raise NotImplementedError

    @abstractmethod
    def list_public_holidays(self, year: int) -> Iterable[date]:
        """Return an iterable of public holiday dates for the given year."""
        raise NotImplementedError

    @abstractmethod
    def list_adjusted_workdays(self, year: int) -> Iterable[date]:
        """Return an iterable of adjusted workday dates for the given year."""
        raise NotImplementedError
