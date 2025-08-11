import unittest
from main import RoomStudentMerger


class TestRoomStudentMerger(unittest.TestCase):
    def setUp(self):
        self.rooms = [
            {"id": 1, "name": "Room #1"},
            {"id": 2, "name": "Room #2"}
        ]
        self.students = [
            {"id": 101, "name": "Alice", "room": 1},
            {"id": 102, "name": "Bob", "room": 2},
            {"id": 103, "name": "Charlie", "room": 3},  # no that room
            {"id": 104, "name": "Diana"}  # no room field
        ]

    def test_students_assigned_to_correct_rooms(self):
        merger = RoomStudentMerger(self.rooms, self.students)
        merged = merger.merge()

        room1 = next(r for r in merged if r['id'] == 1)
        room2 = next(r for r in merged if r['id'] == 2)

        self.assertEqual(len(room1['students']), 1)
        self.assertEqual(room1['students'][0]['name'], 'Alice')

        self.assertEqual(len(room2["students"]), 1)
        self.assertEqual(room2["students"][0]["name"], "Bob")

    def test_students_without_room_go_to_unassigned(self):
        merger = RoomStudentMerger(self.rooms, self.students)
        merged = merger.merge()

        unassigned = next(r for r in merged if r["id"] == "unassigned")
        unassigned_names = [s["name"] for s in unassigned["students"]]

        self.assertIn("Charlie", unassigned_names)
        self.assertIn("Diana", unassigned_names)

    def test_invalid_data_raises_valueerror(self):
        with self.assertRaises(ValueError):
            RoomStudentMerger({}, self.students).merge()

        with self.assertRaises(ValueError):
            RoomStudentMerger(self.rooms, {}).merge()

    def test_empty_rooms_results_in_only_unassigned(self):
        students = [
            {"id": 201, "name": "Eve", "room": 10},
            {"id": 202, "name": "Frank"}
        ]
        merger = RoomStudentMerger([], students)
        merged = merger.merge()

        self.assertEqual(len(merged), 1)  # только Unassigned
        self.assertEqual(merged[0]["id"], "unassigned")
        self.assertEqual(len(merged[0]["students"]), 2)
        names = [s["name"] for s in merged[0]["students"]]
        self.assertIn("Eve", names)
        self.assertIn("Frank", names)


if __name__ == '__main__':
    unittest.main()