# Lab 7 — Fuzzing for Input Validation Bugs

## Files
- `processor.py` — hardened implementation of the three supplied functions.
- `test_processor.py` — Hypothesis property-based fuzz tests and boundary tests.
- `README_LAB7.txt` — run instructions and screenshot checklist.

## Install
```powershell
python -m pip install pytest hypothesis
```

## Capture the required initial failure evidence
Use the original buggy `processor.py` from the assigned team starter repository
(`SETAPESU26/L6_L7_07_hospital_traige_priority`, `Lab 7/processor.py`) and the
completed `test_processor.py` to run:
```powershell
python -m pytest -q test_processor.py
```
The starter implementation is intentionally unvalidated; the arbitrary-input
Hypothesis tests should expose exceptions. Save a genuine screenshot of the
failing run as `01_failing_fuzz_tests.png`.

Run the original buggy interactive program:
```powershell
python processor.py
```
Enter sample inputs such as `bad`, `70/0`, and `ICU-X` to observe invalid-input
crashes. Save a genuine screenshot as `02_buggy_application.png`.

## Run the fixed implementation
Replace `processor.py` with the supplied hardened version, then run:
```powershell
python processor.py
```
For example enter `130,95,37`, `70/1.75`, and `ICU-05`.
Save a genuine screenshot as `03_fixed_application.png`.

Run the fuzz suite:
```powershell
python -m pytest -q test_processor.py
```
Save the genuine passing output as `04_passing_fuzz_tests.png`.

## PDF and ZIP
The handout requires a PDF containing the four screenshots, plus the fixed
`processor.py` and updated `test_processor.py`. Capture the screenshots from
your own terminal; do not use fabricated evidence. Insert the four screenshots
in order into a document and export it as `Lab7_Screenshots.pdf`.
Then include that PDF in the final ZIP.

## Git commits
From the repository root, after creating `Lab 7`:
```powershell
git add "Lab 7/test_processor.py"
git commit -m "Lab 7: Add Hypothesis fuzz tests"
git add "Lab 7/processor.py" "Lab 7/04_passing_fuzz_tests.png" "Lab 7/Lab7_Screenshots.pdf"
git commit -m "Lab 7: Fix input validation and add evidence"
git push origin main
```
Only add screenshot/PDF files after you have actually created them.
