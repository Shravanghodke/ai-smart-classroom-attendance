# QA Test Plan

| ID | Test / possible issue | Expected result | Severity | Evidence to attach |
|---|---|---|---|---|
| QA-01 | Very short or empty WAV input | Clear validation message; no crash | Medium | Console output |
| QA-02 | Unknown speaker / low-confidence prediction | Attendance is not marked; manual verification requested | High | Prediction and CSV check |
| QA-03 | Repeated recognition of the same student on one day | Duplicate policy is applied consistently | Medium | CSV before/after |
| QA-04 | Missing or unreadable training folder | Helpful error message; no false attendance entry | Medium | Console output |
| QA-05 | Noisy or different-microphone recording | Recognition limitations are reported; uncertain cases are not automatically accepted | High | Controlled test results |

These are candidate QA issues to create in GitHub. They are not claims that issues have already been created or resolved.

## Acceptance criteria
- Invalid audio is rejected with a useful message.
- Low-confidence predictions do not create attendance records.
- CSV has a header and a timestamp for every accepted record.
- Each issue includes reproduction steps, root-cause notes, a proposed fix, and test evidence.
- No private or non-consensual voice recordings are committed to the repository.
