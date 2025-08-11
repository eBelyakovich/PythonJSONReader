```bash
git clone <REPO_URL>
cd <PROJECT_FOLDER>
```
Launch:
```bash
python -m student_rooms.cli <rooms.json> <students.json> [--format json|xml] [--output файл]
```
Export to JSON:
```bash
python -m student_rooms.cli rooms.json students.json --format json --output result.json
```
Export to XML:
```bash
python -m student_rooms.cli rooms.json students.json --format xml --output result.xml
```