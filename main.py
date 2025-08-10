import argparse
import json
from abc import abstractmethod, ABC
from pathlib import Path
import xml.etree.ElementTree as ET


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
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)


class JSONExporter(DataExporter):
    def export(self, data, output_file: Path):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class XMLExporter(DataExporter):
    def export(self, data, output_file: Path):
        root = ET.Element('rooms')
        for room in data:
            room_el = ET.SubElement(root, 'rooms', id=str(room['id']), name=room['name'])
            students_el = ET.SubElement(room_el, 'students')
            for student in room['students']:
                ET.SubElement(students_el, 'student', id=str(student['id'])).text = student['name']

            tree = ET.ElementTree(root)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)


class RoomStudentMerger:
    def __init__(self, rooms, students):
        self.rooms = rooms
        self.students = students

    def merge(self):
        rooms_dict = {room["id"]: {**room, "students": []} for room in self.rooms}
        for student in self.students:
            room_id = student.get("room")
            if room_id in rooms_dict:
                rooms_dict[room_id]["students"].append(student)
        return list(rooms_dict.values())


def main():
    parser = argparse.ArgumentParser(description="Merge rooms and students data.")
    parser.add_argument("rooms", type=Path, help="Path to rooms.json")
    parser.add_argument("students", type=Path, help="Path to students.json")
    parser.add_argument("--format", choices=["json", "xml"], default="json", help="Output format")
    parser.add_argument("--output", type=Path, default=Path("output.json"), help="Output file path")
    args = parser.parse_args()

    loader = JSONLoader()
    rooms = loader.load(args.rooms)
    students = loader.load(args.students)

    merger = RoomStudentMerger(rooms, students)
    merged_data = merger.merge()

    exporter: DataExporter = JSONExporter() if args.format == "json" else XMLExporter()
    exporter.export(merged_data, args.output)

    print(f"Данные успешно экспортированы в {args.output}")


if __name__ == "__main__":
    main()
