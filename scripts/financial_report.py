from datetime import date
from pathlib import Path
import json


class day_report:
    def __init__(self, report_day: date = date.today()) -> None:
        self._report_date = report_day
        pass

    def __dict__(self) -> dict:
        pass

    def update_report(self) -> None:

        year = self._report_date.year
        month = self._report_date.strftime('%B').lower()
        day = self._report_date.strftime("%d")

        report_rel_path = f"../data/{year}/{month}.json"
        report_abs_path = Path(__file__).parent / report_rel_path

        with open(report_abs_path, "r+") as report_file:
            report = json.load(report_file)
            report["day_info"][day] = [10, 20]
            report_file.seek(0)
            json.dump(report, report_file, indent=4)


if __name__ == "__main__":
    a = day_report()
    a.update_report()
