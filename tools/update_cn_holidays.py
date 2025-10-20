#!/usr/bin/env python3
"""
Helper script to update assets/raw/cn_holidays_2024_2026.json

Usage examples:
- Add dates to a year:
  python tools/update_cn_holidays.py --year 2024 --add-holidays 2024-12-31  --add-workdays 2024-12-29

- Replace lists for a year from files:
  python tools/update_cn_holidays.py --year 2025 --holidays-file holidays_2025.txt --workdays-file workdays_2025.txt

The JSON file is kept sorted and de-duplicated.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "assets" / "raw" / "cn_holidays_2024_2026.json"


def parse_date(s: str) -> str:
    # Validate ISO date
    datetime.strptime(s, "%Y-%m-%d")
    return s


def load_file_lines(path: Path | None) -> List[str]:
    if not path:
        return []
    lines = [parse_date(l.strip()) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(JSON_PATH), help="Path to holiday JSON file")
    ap.add_argument("--year", type=int, required=True, help="Year to update")

    ap.add_argument("--add-holidays", nargs="*", default=[], help="ISO dates to add as public holidays")
    ap.add_argument("--add-workdays", nargs="*", default=[], help="ISO dates to add as adjusted workdays")

    ap.add_argument("--holidays-file", type=str, help="Path to file containing public holiday dates (one per line)")
    ap.add_argument("--workdays-file", type=str, help="Path to file containing adjusted workday dates (one per line)")

    args = ap.parse_args()
    json_path = Path(args.json)

    data = json.loads(json_path.read_text(encoding="utf-8"))
    years = data.setdefault("years", {})
    y = str(args.year)
    ydata = years.setdefault(y, {"public_holidays": [], "adjusted_workdays": []})

    holidays = set(ydata.get("public_holidays", []))
    workdays = set(ydata.get("adjusted_workdays", []))

    holidays_file = load_file_lines(Path(args.holidays_file)) if args.holidays_file else []
    workdays_file = load_file_lines(Path(args.workdays_file)) if args.workdays_file else []

    for d in args.add_holidays + holidays_file:
        holidays.add(parse_date(d))
    for d in args.add_workdays + workdays_file:
        workdays.add(parse_date(d))

    ydata["public_holidays"] = sorted(holidays)
    ydata["adjusted_workdays"] = sorted(workdays)
    years[y] = ydata

    data["years"] = years
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {json_path} for year {y}")


if __name__ == "__main__":
    main()
