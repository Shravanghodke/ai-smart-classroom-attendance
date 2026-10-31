
"""
AI-Based Smart Classroom Attendance System Using Voice Recognition

Training data structure:
data/train/
    student_1/
        recording1.wav
        recording2.wav
    student_2/
        recording1.wav
        recording2.wav

Use voice recordings only with the students' informed consent.
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

import librosa
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


SAMPLE_RATE = 16000
THRESHOLD = 0.60
MIN_AUDIO_SAMPLES = SAMPLE_RATE // 2  # 0.5 seconds


def features(path: Path) -> np.ndarray:
    """Validate an audio file and extract MFCC features."""

    if not path.exists() or not path.is_file():
        raise ValueError(f"Audio file does not exist: {path}")

    try:
        audio, _ = librosa.load(
            str(path),
            sr=SAMPLE_RATE,
            mono=True
        )
    except Exception as exc:
        raise ValueError(
            f"Unable to read audio file: {path}. "
            "Please provide a valid audio recording."
        ) from exc

    if len(audio) == 0:
        raise ValueError(f"Audio recording is empty: {path}")

    if len(audio) < MIN_AUDIO_SAMPLES:
        raise ValueError(
            f"Recording too short (minimum 0.5 seconds): {path}"
        )

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=SAMPLE_RATE,
        n_mfcc=20
    )

    return np.concatenate([
        mfcc.mean(axis=1),
        mfcc.std(axis=1)
    ])


def load_training_data(root: Path):
    """Load valid recordings and validate the training dataset."""

    if not root.exists() or not root.is_dir():
        raise ValueError(
            f"Training directory does not exist: {root}"
        )

    X = []
    y = []

    for person_dir in sorted(root.iterdir()):
        if not person_dir.is_dir():
            continue

        for wav in sorted(person_dir.glob("*.wav")):
            try:
                X.append(features(wav))
                y.append(person_dir.name)
            except ValueError as exc:
                print(f"Skipping {wav}: {exc}")

    if len(set(y)) < 2 or len(X) < 4:
        raise ValueError(
            "Need at least 2 student folders and "
            "4 valid WAV recordings total."
        )

    return np.asarray(X), np.asarray(y)


def train_model(X: np.ndarray, y: np.ndarray):
    """Train an SVM classifier for speaker identification."""

    model = make_pipeline(
        StandardScaler(),
        SVC(
            kernel="rbf",
            probability=True,
            class_weight="balanced",
            random_state=42
        )
    )

    model.fit(X, y)
    return model


def predict_student(model, audio_path: Path):
    """Identify a student only when confidence meets the threshold."""

    sample = features(audio_path).reshape(1, -1)

    probabilities = model.predict_proba(sample)[0]
    best_index = int(np.argmax(probabilities))

    student_id = str(model.classes_[best_index])
    confidence = float(probabilities[best_index])

    if confidence < THRESHOLD:
        return None, confidence

    return student_id, confidence


def mark_attendance(student_id: str, csv_path: Path):
    """Record attendance once per student per calendar day."""

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    existing_records = []

    if csv_path.exists() and csv_path.stat().st_size > 0:
        with csv_path.open(
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            existing_records = list(csv.DictReader(file))

    for record in existing_records:
        if (
            record.get("student_id") == student_id
            and record.get("date") == today
        ):
            print(
                f"Attendance already recorded for "
                f"{student_id} today."
            )
            return

    file_exists = (
        csv_path.exists() and csv_path.stat().st_size > 0
    )

    with csv_path.open(
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["student_id", "date", "timestamp"]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "student_id": student_id,
            "date": today,
            "timestamp": timestamp
        })

    print(f"Attendance marked for {student_id}.")


def main():
    parser = argparse.ArgumentParser(
        description="AI Smart Classroom Voice Attendance"
    )

    parser.add_argument(
        "--train",
        type=Path,
        default=Path("data/train"),
        help="Directory containing student folders and WAV files"
    )

    parser.add_argument(
        "--test",
        type=Path,
        required=True,
        help="Path to the WAV recording to identify"
    )

    parser.add_argument(
        "--attendance",
        type=Path,
        default=Path("attendance.csv"),
        help="CSV file where attendance will be stored"
    )

    args = parser.parse_args()

    try:
        X, y = load_training_data(args.train)
        model = train_model(X, y)

        student_id, confidence = predict_student(
            model,
            args.test
        )

        print(f"Prediction confidence: {confidence:.2%}")

        if student_id is None:
            print(
                "Low-confidence prediction. Attendance not marked; "
                "manual review required."
            )
            return

        mark_attendance(student_id, args.attendance)

    except (ValueError, OSError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
