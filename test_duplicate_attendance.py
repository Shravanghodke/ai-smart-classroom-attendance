
import csv
import tempfile
from pathlib import Path

from ai.ai_voice_attendance import mark_attendance


def test_duplicate_attendance():
    # Use a temporary folder so the real attendance file is untouched.
    with tempfile.TemporaryDirectory() as temp_dir:
        attendance_file = Path(temp_dir) / "attendance.csv"

        student_id = "student_test"

        # Mark attendance for the first time.
        mark_attendance(student_id, attendance_file)

        # Try marking attendance again on the same day.
        mark_attendance(student_id, attendance_file)

        # Read the CSV and verify that only one record exists.
        with attendance_file.open(
            "r", newline="", encoding="utf-8"
        ) as file:
            records = list(csv.DictReader(file))

        assert len(records) == 1, (
            f"Expected 1 record, but found {len(records)}"
        )
        assert records[0]["student_id"] == student_id

        print("PASS: Duplicate attendance was prevented.")
        print("PASS: Only one attendance record exists.")


if __name__ == "__main__":
    test_duplicate_attendance()
