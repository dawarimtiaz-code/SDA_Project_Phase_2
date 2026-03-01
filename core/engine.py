from typing import List, Any
from .contracts import DataSink, PipelineService
import statistics

class TransformationEngine(PipelineService):
    def _init_(self, sink: DataSink, continent: str, year: int, start_year: int, end_year: int, decline_years: int):
        self.sink = sink
        self.continent = continent
        self.year = year
        self.start_year = start_year
        self.end_year = end_year
        self.decline_years = decline_years

    def execute(self, raw_data: List[Any]) -> None:
        header = raw_data[0]
        continent_index = header.index("Continent")

        continent_records = []
        all_records = []
        for row in raw_data[1:]:
            try:
                yearly_data = {}
                for i, col in enumerate(header[4:-1], start=4):
                    if row[i] != "":
                        yearly_data[int(col)] = float(row[i])
                record = {"Country": row[0], "Continent": row[continent_index], "GDPs": yearly_data}
                all_records.append(record)
                if row[continent_index] == self.continent:
                    continent_records.append(record)
            except Exception:
                continue

        output = {
            "Top 10": self.top_countries(continent_records, self.year),
            "Bottom 10": self.bottom_countries(continent_records, self.year),
            "Growth Rate": self.gdp_growth_rates(continent_records),
            "Avg GDP by Continent": self.average_gdp_by_continent(all_records, self.start_year, self.end_year),
            "Global GDP Trend": self.global_gdp_trend(all_records, self.start_year, self.end_year),
            "Fastest Continent": self.fastest_growing_continent(all_records, self.start_year, self.end_year),
            "Consistent Decline": self.consistent_decline(continent_records),
            "Continent Contribution": self.continent_contributions(all_records, self.start_year, self.end_year)
        }

        self.sink.write(output)

    def top_countries(self, records, year):
        filtered = [{"Country": r["Country"], "GDP": r["GDPs"].get(year, 0)} for r in records if year in r["GDPs"]]
        return sorted(filtered, key=lambda x: x["GDP"], reverse=True)[:10]

    def bottom_countries(self, records, year):
        filtered = [{"Country": r["Country"], "GDP": r["GDPs"].get(year, 0)} for r in records if year in r["GDPs"]]
        return sorted(filtered, key=lambda x: x["GDP"])[:10]

    def gdp_growth_rates(self, records):
        growth = {}
        for r in records:
            years = [y for y in sorted(r["GDPs"].keys()) if self.start_year <= y <= self.end_year]
            if len(years) >= 2:
                first, last = years[0], years[-1]
                g_rate = ((r["GDPs"][last] - r["GDPs"][first]) / r["GDPs"][first]) * 100 if r["GDPs"][first] > 0 else 0
                growth[r["Country"]] = g_rate
        return growth

    def average_gdp_by_continent(self, records, start_year, end_year):
        continent_avgs = {}
        for r in records:
            values = [r["GDPs"][y] for y in r["GDPs"] if start_year <= y <= end_year]
            if values:
                continent_avgs.setdefault(r["Continent"], []).extend(values)
        return {c: statistics.mean(vals) for c, vals in continent_avgs.items()}

    def global_gdp_trend(self, records, start_year, end_year):
        trend = {}
        for r in records:
            for y, val in r["GDPs"].items():
                if start_year <= y <= end_year:
                    trend[y] = trend.get(y, 0) + val
        return dict(sorted(trend.items()))

    def fastest_growing_continent(self, records, start_year, end_year):
        continent_growth = {}
        for r in records:
            years = [y for y in sorted(r["GDPs"].keys()) if start_year <= y <= end_year]
            if len(years) >= 2:
                first, last = years[0], years[-1]
                growth = ((r["GDPs"][last] - r["GDPs"][first]) / r["GDPs"][first]) * 100 if r["GDPs"][first] > 0 else 0
                continent_growth[r["Continent"]] = continent_growth.get(r["Continent"], 0) + growth
        return max(continent_growth, key=continent_growth.get) if continent_growth else "N/A"

    def consistent_decline(self, records):
        declining = []
        for r in records:
            years = sorted(r["GDPs"].keys())[-self.decline_years:]
            if len(years) == self.decline_years:
                values = [r["GDPs"][y] for y in years]
                if all(values[i] > values[i+1] for i in range(len(values)-1)):
                    declining.append(r["Country"])
        return declining

    def continent_contributions(self, records, start_year, end_year):
        totals = {}
        global_total = 0
        for r in records:
            for y, val in r["GDPs"].items():
                if start_year <= y <= end_year:
                    totals[r["Continent"]] = totals.get(r["Continent"], 0) + val
                    global_total += val
        return {c: (val/global_total)*100 for c, val in totals.items()} if global_total > 0 else {}