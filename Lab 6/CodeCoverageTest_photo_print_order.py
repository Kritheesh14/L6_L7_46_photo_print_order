import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------
def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_unknown_print_size():
    with pytest.raises(ValueError):
        extra_print_charge("2x2", 5, "matte", False)


def test_negative_copies():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_member_bonus_matte():
    # 4x6 member: included = 25, extra = 5, matte rate 4 -> 20
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_non_matte_rate():
    # 4x6 non-member: included = 20, extra = 5, glossy rate 7 -> 35
    assert extra_print_charge("4x6", 25, "glossy", False) == 35


def test_bulk_canvas_surcharge():
    # 4x6 non-member: extra = 60, rate 7 + 2 + 5 = 14 -> 840
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


# ---------- order_valid ----------
def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_order():
    assert order_valid(10, 40, True) is True


def test_file_too_large():
    assert order_valid(30, 100, False) is False


# ---------- dispatch_status ----------
def test_dispatch_on_time():
    assert dispatch_status(12, False, False) == "on_time"


def test_dispatch_tight():
    assert dispatch_status(8, False, False) == "tight"


def test_dispatch_missed():
    assert dispatch_status(2, False, False) == "missed"


def test_dispatch_framed_international():
    assert dispatch_status(48, True, True) == "on_time"