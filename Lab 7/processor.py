"""Validated input processors for the Hospital Triage Priority lab."""
import math


def _finite_float(value):
    """Convert a value to a finite float, otherwise return None."""
    try:
        number = float(value.strip())
    except (AttributeError, TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def parse_vitals_summary(vitals_csv):
    """Parse 'heart_rate,spo2,temperature'; return None for invalid input."""
    if not isinstance(vitals_csv, str) or not vitals_csv.strip():
        return None

    parts = vitals_csv.split(",")
    if len(parts) != 3:
        return None

    hr = _finite_float(parts[0])
    spo2 = _finite_float(parts[1])
    temp = _finite_float(parts[2])
    if hr is None or spo2 is None or temp is None:
        return None

    # Physiological values must be in plausible, non-negative ranges.
    if not (0 < hr <= 300 and 0 <= spo2 <= 100 and 0 < temp <= 60):
        return None

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return (
        f"Vitals: HR={hr}, SpO2={spo2}% - "
        f"{'CRITICAL' if critical else 'STABLE'}"
    )


def compute_patient_bmi(bmi_string):
    """Parse 'weight/height' in kg/metres and return BMI rounded to 2 decimals."""
    if not isinstance(bmi_string, str) or not bmi_string.strip():
        return None

    parts = bmi_string.split("/")
    if len(parts) != 2:
        return None

    weight = _finite_float(parts[0])
    height = _finite_float(parts[1])
    if weight is None or height is None or weight <= 0 or height <= 0:
        return None

    # Avoid overflow in height**2 and division by zero/overflow.
    try:
        bmi = weight / (height * height)
    except (ArithmeticError, OverflowError):
        return None
    if not math.isfinite(bmi):
        return None
    return round(bmi, 2)


def assign_ward_bed(allocation_code):
    """Parse a ward-bed code such as ICU-05; invalid codes return None."""
    if not isinstance(allocation_code, str) or not allocation_code.strip():
        return None

    parts = allocation_code.strip().split("-")
    if len(parts) != 2:
        return None

    ward = parts[0].strip().upper()
    bed_str = parts[1].strip()
    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics",
    }
    if ward not in ward_names or not bed_str:
        return None

    # Accept positive decimal digits only (not signs or decimal notation).
    if not bed_str.isdecimal():
        return None
    try:
        bed_num = int(bed_str)
    except (ValueError, OverflowError):
        return None
    if bed_num <= 0:
        return None

    return f"{ward_names[ward]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    result = parse_vitals_summary(v_input)
    print("Summary:", result if result is not None else "Invalid vitals input")

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    result = compute_patient_bmi(b_input)
    print("BMI:", result if result is not None else "Invalid BMI input")

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    result = assign_ward_bed(w_input)
    print("Assignment:", result if result is not None else "Invalid allocation code")


if __name__ == "__main__":
    main()
