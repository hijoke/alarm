from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterable, Set

from .provider import HolidayProvider


@dataclass
class _YearData:
    public_holidays: Set[date]
    adjusted_workdays: Set[date]


class CNHolidayProvider(HolidayProvider):
    """
    Default CN holiday provider reading from a bundled JSON file in assets/raw.

    JSON structure:
    {
      "country": "CN",
      "years": {
        "2024": {
          "public_holidays": ["2024-01-01", ...],
          "adjusted_workdays": ["2024-02-04", ...]
        },
        ...
      }
    }
    """

    def __init__(self, data_path: Path | None = None) -> None:
        if data_path is None:
            data_path = Path(__file__).resolve().parents[1] / "assets" / "raw" / "cn_holidays_2024_2026.json"
        self._data_path = data_path
        self._years: Dict[int, _YearData] = {}
        self._load()

    def _parse_date(self, s: str) -> date:
        return datetime.strptime(s, "%Y-%m-%d").date()

    def _load(self) -> None:
        with self._data_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        years = raw.get("years", {})
        for y_str, y_data in years.items():
            y = int(y_str)
            ph = {self._parse_date(d) for d in y_data.get("public_holidays", [])}
            aw = {self._parse_date(d) for d in y_data.get("adjusted_workdays", [])}
            self._years[y] = _YearData(public_holidays=ph, adjusted_workdays=aw)

    def _get_year_data(self, year: int) -> _YearData:
        return self._years.get(year, _YearData(public_holidays=set(), adjusted_workdays=set()))

    def is_public_holiday(self, d: date) -> bool:
        yd = self._get_year_data(d.year)
        return d in yd.public_holidays

    def is_adjusted_workday(self, d: date) -> bool:
        yd = self._get_year_data(d.year)
        return d in yd.adjusted_workdays

    def list_public_holidays(self, year: int) -> Iterable[date]:
        return sorted(self._get_year_data(year).public_holidays)

    def list_adjusted_workdays(self, year: int) -> Iterable[date]:
        return sorted(self._get_year_data(year).adjusted_workdays)
