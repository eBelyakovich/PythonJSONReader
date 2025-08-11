import argparse
import json
from abc import abstractmethod, ABC
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom


class DataLoader(ABC):
    @abstractmethod
    def load(self, file_path: Path):
        pass


class DataExporter(ABC):
    @abstractmethod
    def export(self, data, output_file: Path):
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


class JSONExporter(DataExporter):
    def export(self, data, output_file: Path):
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise IOError(f"Write error: {e}")


class XMLExporter(DataExporter):
    def export(self, data, output_file: Path):
        try:
            root = ET.Element("rooms")
            for room in data:
                room_el = ET.SubElement(
                    root, "room", id=str(room["id"]), name=room["name"]
                )
                students_el = ET.SubElement(room_el, "students")
                for student in room["students"]:
                    student_el = ET.SubElement(
                        students_el, "student", id=str(student["id"])
                    )
                    student_el.text = student["name"]

            rough_string = ET.tostring(root, encoding="utf-8")
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")

            with open(output_file, "wb") as f:
                f.write(pretty_xml)

        except Exception as e:
            raise IOError(f"Error XML writing: {e}")


class RoomStudentMerger:
    def __init__(self, rooms, students):
        self.rooms = rooms
        self.students = students

    def merge(self):
        if not isinstance(self.rooms, list) or not isinstance(self.students, list):
            raise ValueError("Wrong format of data: expect list of students and rooms")
        rooms_dict = {room["id"]: {**room, "students": []} for room in self.rooms}
        unassigned_id = "unassigned"
        rooms_dict[unassigned_id] = {
            "id": unassigned_id,
            "name": "Unassigned",
            "students": [],
        }
        for student in self.students:
            room_id = student.get("room")
            if room_id in rooms_dict:
                rooms_dict[room_id]["students"].append(student)
            else:
                rooms_dict[unassigned_id]["students"].append(student)
        return list(rooms_dict.values())


def main():
    parser = argparse.ArgumentParser(description="Merge rooms and students data.")
    parser.add_argument("rooms", type=Path, help="Path to rooms.json")
    parser.add_argument("students", type=Path, help="Path to students.json")
    parser.add_argument(
        "--format", choices=["json", "xml"], default="json", help="Output format"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("output.json"), help="Output file path"
    )
    args = parser.parse_args()

    try:
        loader = JSONLoader()
        rooms = loader.load(args.rooms)
        students = loader.load(args.students)

        merger = RoomStudentMerger(rooms, students)
        merged_data = merger.merge()

        exporter: DataExporter = (
            JSONExporter() if args.format == "json" else XMLExporter()
        )
        exporter.export(merged_data, args.output)

        print(f"Data export success in: {args.output}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
