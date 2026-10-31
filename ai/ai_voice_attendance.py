"""Educational speaker-identification demo using MFCC features and an SVM.

Expected training layout:
data/train/student_001/*.wav
data/train/student_002/*.wav

Use consented audio only. This is not a production biometric system.
"""
import argparse
import csv
from datetime import datetime
from pathlib import Path

import librosa
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC

SAMPLE_RATE = 16000
THRESHOLD = 0.60

def features(path: Path) -> np.ndarray:
    audio, _ = librosa.load(path, sr=SAMPLE_RATE, mono=True)
    if len(audio) < SAMPLE_RATE // 2:
        raise ValueError(f"Recording too short (minimum 0.5 seconds): {path}")
    mfcc = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=20)
    # Mean and standard deviation make a fixed-length feature vector.
    return np.concatenate([mfcc.mean(axis=1), mfcc.std(axis=1)])

def load_training_data(root: Path):
    X, y = [], []
    for person_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for wav in sorted(person_dir.glob("*.wav")):
            try:
                X.append(features(wav))
                y.append(person_dir.name)
            except Exception as exc:
                print(f"Skipping {wav}: {exc}")
    if len(set(y)) < 2 or len(X) < 4:
        raise ValueError("Need at least 2 student folders and 4 valid WAV recordings total.")
    return np.asarray(X), np.asarray(y)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", type=Path, required=True, help="Folder containing one subfolder per student")
    parser.add_argument("--test", type=Path, required=True, help="WAV file to identify")
    parser.add_argument("--attendance", type=Path, default=Path("attendance.csv"))
    args = parser.parse_args()

    X, labels = load_training_data(args.train)
    encoder = LabelEncoder()
    y = encoder.fit_transform(labels)
    model = make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True, random_state=42))
    model.fit(X, y)

    test_x = features(args.test).reshape(1, -1)
    probabilities = model.predict_proba(test_x)[0]
    best_index = int(np.argmax(probabilities))
    student_id = encoder.inverse_transform([model.classes_[best_index]])[0]
    confidence = float(probabilities[best_index])
    print(f"Prediction: {student_id}; confidence={confidence:.2f}")

    if confidence < THRESHOLD:
        print("Low confidence: attendance NOT marked. Please verify manually.")
        return

    args.attendance.parent.mkdir(parents=True, exist_ok=True)
    new_file = not args.attendance.exists()
    with args.attendance.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "student_id", "confidence", "audio_file"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), student_id,
                         f"{confidence:.3f}", args.test.name])
    print(f"Attendance recorded in {args.attendance}")

if __name__ == "__main__":
    main()
