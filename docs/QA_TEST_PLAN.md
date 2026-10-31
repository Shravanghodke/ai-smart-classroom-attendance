# QA Test Plan

| ID | Test / possible issue | Expected result | Severity | Evidence to attach |
|---|---|---|---|---|
### QA-01: Short Audio Recording

-Test 1 input: 0.1-second silent WAV file (short_test.wav).

Test 1 actual result: The program raised ValueError: Recording too short (minimum 0.5 seconds): short_test.wav.

Test 1 status: PASS.

- **Test input:** Zero-second WAV file (`empty_test.wav`).
- **Actual result:** The program rejected the empty recording with a clear validation error.
- **Status:** PASS.
- **Evidence:** Screenshot of the VS Code terminal.

Evidence: VS Code terminal screenshots showing both test results.
### QA-02 | 
**Additional unit test — confidence threshold**

- Input confidence values: 0.42, 0.85, and 0.60.
- Expected result: Reject 0.42; accept 0.85 and 0.60.
- Actual result: Record the terminal output.
- Status: PASS if all three assertions succeed.
- Limitation: This tests the threshold decision independently, not end-to-end speaker recognition or attendance prevention.

### QA-03 | Prevent Duplicate Attendance Records

Status: PASS

Test performed: Called mark_attendance() twice for the same student on the same day using a temporary CSV file.

Expected result: The first attempt records attendance, and the second attempt is rejected as a duplicate.

Actual result: Only one attendance record was created. The duplicate attempt was prevented successfully.

Evidence: test_duplicate_attendance.py passed both assertions, confirming that duplicate attendance was prevented and only one record existed.

Limitation: This test validates CSV attendance-record handling, not the complete voice-recognition pipeline.
### QA-04 | Missing or unreadable training folder | Test input: Empty training folder.

Expected result: The program should stop and display a clear validation error.

Actual result: The program raised a ValueError stating that at least 2 student folders and 4 valid WAV recordings are required.

Status: PASS — the program correctly rejected insufficient training data.

Evidence: Screenshot of the VS Code terminal showing the command and error message.
| QA-05 | Noisy or different-microphone recording | Recognition limitations are reported; uncertain cases are not automatically accepted | High | Controlled test results |

These are candidate QA issues to create in GitHub. They are not claims that issues have already been created or resolved.

## Acceptance criteria
- Invalid audio is rejected with a useful message.
- Low-confidence predictions do not create attendance records.
- CSV has a header and a timestamp for every accepted record.
- Each issue includes reproduction steps, root-cause notes, a proposed fix, and test evidence.
- No private or non-consensual voice recordings are committed to the repository.
