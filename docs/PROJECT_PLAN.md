# Project Planning and Tracking

## Scope
Build a demonstrator combining an optional ESP32/PIR presence signal with AI-based speaker identification and local attendance logging.

## Work breakdown
| Task | Planned duration | Dependency | Status |
|---|---:|---|---|
| Create repository and README | 0.5 day | None | Starter files prepared; GitHub upload pending |
| Test ESP32/PIR sketch | 0.5 day | Hardware available | Pending hardware test |
| Collect consented sample audio | 1 day | Consent and privacy plan | Pending |
| Train/test MFCC + SVM baseline | 1 day | Audio dataset | Pending validation |
| Run QA tests and open GitHub Issues | 1 day | Repository created | Pending |
| Document fixes and close verified issues | 0.5 day | QA test results | Pending |
| Finalize report and Moodle submission | 0.5 day | Real repo/issues evidence | Pending |

## Tracking method
Use GitHub Issues for defects, labels for severity (`high`, `medium`, `low`), milestones for phases, and commits that reference issue numbers (for example, `Fixes #2`). Close issues only after retesting and adding evidence.

## Risks
- Small or unbalanced voice datasets can cause misidentification.
- Background noise and microphone variation reduce accuracy.
- Voice data is sensitive biometric data; use informed consent, restrict access, and delete recordings when no longer needed.
- The ESP32/PIR sketch detects motion only; it does not perform speaker identification.
