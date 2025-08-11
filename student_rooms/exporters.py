import json
import xml.etree.ElementTree as ET
from pathlib import Path
from abc import ABC, abstractmethod
from xml.dom import minidom


class DataExporter(ABC):
    @abstractmethod
    def export(self, data, output_file: Path):
        pass


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
