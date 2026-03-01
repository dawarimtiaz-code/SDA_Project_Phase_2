import json
from core.engine import TransformationEngine
from plugins.inputs import CSVReader, JSONReader
from plugins.outputs import DashboardWriter

INPUT_DRIVERS = {
    "csv": CSVReader,
    "json": JSONReader
}

OUTPUT_DRIVERS = {
    "dashboard": DashboardWriter
}

def bootstrap():
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    input_type = config["input"]["type"]
    filepath = config["input"]["file_path"]

    output_type = config["output"]["type"]

    analysis = config["analysis"]
    continent = analysis["continent"]
    year = analysis["year"]
    start_year = analysis["start_year"]
    end_year = analysis["end_year"]
    decline_years = analysis["decline_years"]

    sink_class = OUTPUT_DRIVERS[output_type]
    sink = sink_class()

    core = TransformationEngine(sink, continent, year, start_year, end_year, decline_years)

    input_class = INPUT_DRIVERS[input_type]
    input_driver = input_class(filepath, core)

    input_driver.run()

if _name_ == "_main_":
    bootstrap()