from hypothesis import given, strategies as st
from photo_print_order import parse_order, file_size_average, payable_amount


# ---------- 1. Fuzz: functions must never crash ----------
@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"


@given(st.text() | st.none())
def test_file_size_average_no_crash(s):
    try:
        file_size_average(s)
    except Exception as e:
        assert False, f"file_size_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_amount_no_crash(s):
    try:
        payable_amount(s)
    except Exception as e:
        assert False, f"payable_amount crashed with: {e!r}"


# ---------- 2. Fuzz with non-text inputs as well ----------
@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()), st.booleans(), st.binary()))
def test_all_functions_survive_non_string_input(x):
    for func in (parse_order, file_size_average, payable_amount):
        try:
            func(x)
        except Exception as e:
            assert False, f"{func.__name__} crashed with: {e!r}"


# ---------- 3. Property tests: valid input gives correct output ----------
@given(st.from_regex(r"[0-9]{1,2}x[0-9]{1,2}", fullmatch=True),
       st.integers(min_value=0, max_value=10**6))
def test_parse_order_valid_roundtrip(size, copies):
    assert parse_order(f"{size}:{copies}") == (size.upper(), copies)


@given(st.lists(st.integers(min_value=0, max_value=10**4), min_size=1, max_size=20))
def test_file_size_average_within_min_and_max(values):
    result = file_size_average(",".join(map(str, values)))
    assert min(values) <= result <= max(values)


@given(st.floats(min_value=0, max_value=1e9, allow_nan=False),
       st.floats(min_value=0, max_value=1e9, allow_nan=False))
def test_payable_amount_never_negative(amount, discount):
    result = payable_amount(f"{amount}|{discount}")
    assert result is not None and result >= 0


# ---------- 4. Specific edge cases found by fuzzing ----------
def test_known_good_values():
    assert parse_order("4x6:25") == ("4X6", 25)
    assert file_size_average("4,8,12") == 8
    assert abs(payable_amount("450|50") - 481.0) < 1e-9


def test_known_bad_values_return_none():
    assert parse_order("4x6") is None            # no colon
    assert parse_order("4x6:abc") is None        # copies not a number
    assert parse_order("a:b:c") is None          # too many colons
    assert parse_order("4x6:-5") is None         # negative copies
    assert file_size_average("") is None         # empty input
    assert file_size_average("1,,3") is None     # empty element
    assert file_size_average("one,two") is None  # not numbers
    assert payable_amount("100") is None         # missing separator
    assert payable_amount("nan|0") is None       # NaN rejected
    assert payable_amount("inf|0") is None       # infinity rejected