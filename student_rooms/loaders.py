import json
from abc import ABC, abstractmethod
from pathlib import Path


class DataLoader(ABC):
    @abstractmethod
    def load(self, file_path: Path):
        pass


class JSONLoader(DataLoader):
    def load(self, file_path: Path):
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file {file_path}: {e}")
