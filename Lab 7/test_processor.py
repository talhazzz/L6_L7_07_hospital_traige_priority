from hypothesis import given, strategies as st
from processor import (
    parse_vitals_summary,
    compute_patient_bmi,
    assign_ward_bed,
)


# Fuzz arbitrary text and None: each public function must fail safely.
@given(st.one_of(st.text(), st.none()))
def test_parse_vitals_summary_no_crash(value):
    result = parse_vitals_summary(value)
    assert result is None or isinstance(result, str)


@given(st.one_of(st.text(), st.none()))
def test_compute_patient_bmi_safe(value):
    result = compute_patient_bmi(value)
    assert result is None or (
        isinstance(result, float) and result >= 0
    )


@given(st.one_of(st.text(), st.none()))
def test_assign_ward_bed_safe(value):
    result = assign_ward_bed(value)
    assert result is None or isinstance(result, str)


# Structured valid and boundary inputs test expected behaviour too.
@given(
    hr=st.floats(min_value=0.01, max_value=300, allow_nan=False, allow_infinity=False),
    spo2=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    temp=st.floats(min_value=0.01, max_value=60, allow_nan=False, allow_infinity=False),
)
def test_valid_vitals_always_return_summary(hr, spo2, temp):
    result = parse_vitals_summary(f"{hr},{spo2},{temp}")
    assert result.startswith("Vitals: HR=")
    assert result.endswith(("CRITICAL", "STABLE"))


@given(
    weight=st.floats(min_value=0.01, max_value=500, allow_nan=False, allow_infinity=False),
    height=st.floats(min_value=0.1, max_value=2.8, allow_nan=False, allow_infinity=False),
)
def test_valid_bmi_is_finite_nonnegative(weight, height):
    result = compute_patient_bmi(f"{weight}/{height}")
    assert isinstance(result, float)
    assert result >= 0


@given(
    ward=st.sampled_from(["ER", "ICU", "GEN", "PED"]),
    bed=st.integers(min_value=1, max_value=99999),
)
def test_valid_ward_bed_codes(ward, bed):
    result = assign_ward_bed(f"{ward}-{bed:02d}")
    assert result.endswith(f"Bed #{bed}")


def test_known_examples():
    assert "CRITICAL" in parse_vitals_summary("130,95,37")
    assert compute_patient_bmi("70/1.75") == 22.86
    assert assign_ward_bed("ICU-05") == "Intensive Care Unit Bed #5"


def test_invalid_values_return_none():
    assert parse_vitals_summary("1,2") is None
    assert parse_vitals_summary("nan,90,37") is None
    assert compute_patient_bmi("70/0") is None
    assert compute_patient_bmi("inf/1.7") is None
    assert assign_ward_bed("XYZ-2") is None
    assert assign_ward_bed("ICU-0") is None
