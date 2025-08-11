import argparse
import os
from pathlib import Path
from .loaders import JSONLoader
from .exporters import JSONExporter, XMLExporter
from .merger import RoomStudentMerger


EXPORTERS = {
    "json": JSONExporter,
    "xml": XMLExporter
}


def parse_args():
    parser = argparse.ArgumentParser(description="Merge rooms and students data.")
    parser.add_argument("rooms", type=Path, help="Path to rooms.json")
    parser.add_argument("students", type=Path, help="Path to students.json")
    parser.add_argument("--format", choices=EXPORTERS.keys(), default="json", help="Output format")
    parser.add_argument("--output", type=Path, default=Path("output.json"), help="Output file path")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        loader = JSONLoader()
        rooms = loader.load(args.rooms)
        students = loader.load(args.students)

        merger = RoomStudentMerger(rooms, students)
        merged_data = merger.merge()

        exporter_class = EXPORTERS[args.format]
        exporter = exporter_class()
        exporter.export(merged_data, args.output)

        abs_path = os.path.abspath(args.output)
        print(f"Data export success in: {abs_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()