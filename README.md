# AI-Based Smart Classroom Attendance System (Starter Repository)

**Purpose:** A small AI-based project concept for the Project Management activity on GitHub QA documentation and problem solving.

## What it does
- Uses an ESP32 + PIR sensor as an optional classroom-presence signal.
- Uses a Python speaker-identification pipeline to classify enrolled speakers from audio recordings.
- Logs attendance locally to `attendance.csv` after a successful match.
- Uses GitHub Issues to record defects, root causes, fixes, and test evidence.

> **Prototype notice:** Speaker recognition is a biometric technology. Use consented recordings only, protect the dataset, and do not use this prototype for high-stakes attendance decisions without human review. The included model is a classroom demonstration, not a production-ready identity system.

## Repository structure
- `arduino/esp32_presence.ino` — ESP32 PIR sensor presence indicator (optional hardware component).
- `ai/ai_voice_attendance.py` — MFCC + SVM speaker-identification demo.
- `.github/ISSUE_TEMPLATE/bug_report.md` — structured QA issue template.
- `docs/QA_TEST_PLAN.md` — test plan and acceptance criteria.
- `docs/PROJECT_PLAN.md` — project planning and tracking.

## Setup (AI demo)
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`
3. Prepare data folders as `data/train/<student_id>/*.wav`. Each enrolled student should have multiple consented recordings.
4. Run: `python ai/ai_voice_attendance.py --train data/train --test path/to/test.wav`
5. If the model predicts a known speaker above the configured confidence threshold, the script appends a record to `attendance.csv`.

The audio files should be mono WAV recordings with reasonably consistent sampling conditions. Results depend heavily on recording quality and dataset size.

## GitHub workflow
1. Create a public or private GitHub repository named `ai-smart-classroom-attendance`.
2. Upload these files or push this folder using Git.
3. Open **Issues** and create issues from the QA list in the report / `docs/QA_TEST_PLAN.md`.
4. Comment with root cause, fix, and test evidence. Close an issue only after verifying the fix.
5. Add the real repository URL and real issue numbers to the report before Moodle submission.
