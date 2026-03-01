import csv
import json
from typing import Any, List
from core.contracts import PipelineService

class CSVReader:
    def _init_(self, filepath: str, service: PipelineService):
        self.filepath = filepath
        self.service = service

    def run(self) -> None:
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data: List[Any] = list(reader)
        self.service.execute(data)

class JSONReader:
    def _init_(self, filepath: str, service: PipelineService):
        self.filepath = filepath
        self.service = service

    def run(self) -> None:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.service.execute(data)