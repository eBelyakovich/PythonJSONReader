from collections import defaultdict


class RoomStudentMerger:
    def __init__(self, rooms, students):
        self.rooms = rooms
        self.students = students

    def merge(self):
        if not isinstance(self.rooms, list) or not isinstance(self.students, list):
            raise ValueError("Wrong format of data: expect list of students and rooms")

        rooms_dict = defaultdict(lambda: {"students": []})

        for room in self.rooms:
            rooms_dict[room["id"]] = {**room, "students": []}

        unassigned_id = "unassigned"
        rooms_dict[unassigned_id] = {"id": unassigned_id, "name": "Unassigned", "students": []}

        for student in self.students:
            room_id = student.get("room")
            if room_id in rooms_dict:
                rooms_dict[room_id]["students"].append(student)
            else:
                rooms_dict[unassigned_id]["students"].append(student)

        return list(rooms_dict.values())
