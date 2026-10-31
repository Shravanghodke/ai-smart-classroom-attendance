
# QA Test Plan
## AI-Based Smart Classroom Attendance System Using Voice Recognition

**Repository:** https://github.com/Shravanghodke/ai-smart-classroom-attendance

**Project type:** AI / Machine Learning / Embedded Systems

**Purpose:** To test audio validation, speaker identification, attendance recording, and error handling.

---

## 1. Project Overview

The project uses MFCC (Mel-Frequency Cepstral Coefficients) for audio feature extraction and an SVM (Support Vector Machine) classifier for speaker identification.

The system aims to identify a student from a voice recording and record attendance only when the prediction confidence meets the configured threshold.

The ESP32 and PIR sensor are optional classroom-presence components. They do not independently identify a student.

## 2. QA Test Summary

| Test ID | Test case | Priority | Current status |
|---|---|---|---|
| QA-01 | Short or empty audio recording | Medium | PASS - tested |
| QA-02 | Reject low-confidence prediction | High | Not tested |
| QA-03 | Prevent duplicate attendance | Medium | Not tested |
| QA-04 | Missing or insufficient training data | Medium | PASS - tested |
| QA-05 | Speaker recognition in noisy conditions | High | Not tested |

**Note:** PASS applies only to the specific test inputs described below. It does not mean every possible case has been tested.

## 3. Detailed Test Cases

### QA-01: Handle Short or Empty Audio Recordings

**GitHub issue:** #1

**Problem:** Short or empty recordings may not contain enough audio information for reliable feature extraction.

**Test A — Short recording**

- Test input: `short_test.wav`, a 0.1-second silent WAV file.
- Expected result: The recording should be rejected because it is shorter than 0.5 seconds.
- Actual result: The program raised a `ValueError` indicating that the recording was too short.
- Status: PASS.

**Test B — Empty recording**

- Test input: `empty_test.wav`, a zero-second WAV file.
- Expected result: The program should reject the empty recording with a clear validation message.
- Actual result: After updating the validation function, the program displayed an error indicating that the audio recording was empty.
- Status: PASS.

**Root cause:** Audio input must be validated before MFCC feature extraction.

**Solution implemented:** Added checks for missing files, unreadable audio, empty recordings, and recordings shorter than 0.5 seconds.

**Evidence:** Attach the VS Code terminal screenshots showing both test results.

### QA-02: Reject Low-Confidence Speaker Predictions

**GitHub issue:** #2

**Problem:** An uncertain speaker prediction could incorrectly mark attendance for the wrong student.

**Expected result:** If the prediction confidence is below the configured threshold of 0.60, attendance should not be marked automatically.

**Root cause:** A classifier prediction should not automatically be treated as a reliable identity when confidence is low.

**Proposed solution:** Check the maximum prediction probability against the threshold and require manual review when it is too low.

**Test procedure:**
1. Prepare valid, consented training recordings for at least two students.
2. Train the model.
3. Test with an appropriate recording that produces a prediction below the threshold.
4. Verify that no attendance entry is created for that prediction.

**Actual result:** Not tested.

**Status:** Not tested.

**Evidence required:** Terminal output and attendance CSV before and after the test.

### QA-03: Prevent Duplicate Attendance Records

**GitHub issue:** #3

**Problem:** Repeated recognition of the same student may create duplicate attendance entries.

**Expected result:** Only one attendance entry should be stored per student per calendar day.

**Root cause:** Repeated recognition events can attempt to insert the same student's attendance more than once.

**Proposed solution:** Check the existing attendance CSV for a matching student ID and date before inserting a new row.

**Test procedure:**
1. Use a valid test setup to identify a student.
2. Mark attendance for that student.
3. Repeat the attendance operation on the same day.
4. Verify that no second row is added.

**Actual result:** Not tested.

**Status:** Not tested.

**Evidence required:** Attendance CSV before and after the repeated operation.

### QA-04: Handle Missing or Insufficient Training Data

**GitHub issue:** #4

**Problem:** The model cannot train reliably when the training dataset is missing or contains too few valid recordings.

**Test input:** Empty `data/train` directory.

**Expected result:** The program should stop and display a clear validation error.

**Actual result:** The program raised a `ValueError` stating that at least two student folders and four valid WAV recordings are required.

**Root cause:** The model requires sufficient valid samples from multiple student classes.

**Solution verified:** The training-data validation stopped the process before model training.

**Status:** PASS for the empty training-folder test.

**Evidence:** Attach the VS Code terminal screenshot showing the validation error.

### QA-05: Test Speaker Recognition Under Noisy Conditions

**GitHub issue:** #5

**Problem:** Background noise may affect MFCC features and reduce speaker-identification reliability.

**Expected result:** Recognition performance should be evaluated under different noise conditions. Uncertain predictions should be flagged for manual review.

**Root cause:** Noise can change the acoustic features extracted from a recording.

**Proposed solution:** Test recordings under quiet and noisy conditions, compare prediction results, and document the limitations.

**Test procedure:**
1. Prepare consented recordings in a quiet environment.
2. Prepare comparable recordings with background noise.
3. Run the same model on the test recordings.
4. Record prediction confidence and identification results.
5. Compare results without claiming accuracy improvements unless measured.

**Actual result:** Not tested.

**Status:** Not tested.

**Evidence required:** Test results, terminal screenshots, and a comparison of the observed predictions.

## 4. Test Environment

- Operating system: Windows.
- Development environment: Visual Studio Code.
- Programming language: Python.
- Audio processing: Librosa.
- Numerical processing: NumPy.
- Machine learning: Scikit-learn.
- Test inputs: Locally generated silent WAV files for audio validation.
- Attendance output: CSV file.

## 5. Collaboration Summary

Collaboration was performed using GitHub Issues. A friend reviewed Issue #1 and recommended validating audio recordings before extracting MFCC features. I replied to the comment and agreed to test short and empty recordings, document the results, and improve error handling where required.

Comments were also added to the other QA issues to discuss low-confidence predictions, duplicate attendance, insufficient training data, and noisy audio.

Screenshots of the GitHub discussion should be attached as evidence of peer review and collaboration.

## 6. Project Planning and Tracking

| Task | Status |
|---|---|
| Create GitHub repository | Completed |
| Upload project files | Completed |
| Create five QA issues | Completed |
| Add collaboration comments | Completed |
| Test short audio recording | Completed |
| Test empty audio recording | Completed |
| Test insufficient training data | Completed |
| Test low-confidence prediction | Pending |
| Test duplicate attendance prevention | Pending |
| Test recognition under noisy conditions | Pending |
| Capture and organize evidence | In progress |
| Finalize activity report | Pending |
| Submit report on Moodle | Pending |

Update these statuses as the remaining work is actually completed.

## 7. Learning Outcomes

Through this activity, I learned how to:

- Create and manage a GitHub repository.
- Document QA issues with expected behavior and proposed solutions.
- Collaborate using GitHub issue comments.
- Test audio-validation and training-data checks.
- Improve Python error handling.
- Maintain a QA test plan and record evidence.
- Track completed and pending project tasks.

## 8. Conclusion

The initial tests confirmed that the program rejects a 0.1-second audio recording, handles an empty audio recording with a clear validation message after the code update, and stops when training data is insufficient.

The remaining tests for low-confidence predictions, duplicate attendance, and noisy conditions still need to be performed. Their outcomes should be recorded after testing, and the associated GitHub issues should be closed only when the relevant behavior has been verified.
