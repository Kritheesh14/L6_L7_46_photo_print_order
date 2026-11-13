import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------
def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_unknown_print_size():
    with pytest.raises(ValueError, match="unknown print size"):
        extra_print_charge("2x2", 5, "matte", False)


def test_negative_copies():
    with pytest.raises(ValueError, match="invalid copies"):
        extra_print_charge("4x6", -1, "matte", False)


def test_zero_copies():
    assert extra_print_charge("4x6", 0, "matte", False) == 0


def test_member_bonus_matte():
    # 4x6 member: included = 25, extra = 5, matte rate 4 -> 20
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_8x10_gets_no_bonus():
    # 8x10 member: included stays 10, extra = 5, matte rate 4 -> 20
    assert extra_print_charge("8x10", 15, "matte", True) == 20


def test_non_member_no_bonus():
    # 5x7 non-member: included = 15, extra = 5, matte rate 4 -> 20
    assert extra_print_charge("5x7", 20, "matte", False) == 20


def test_extra_exactly_zero_boundary():
    # 4x6 non-member: copies == included -> extra = 0
    assert extra_print_charge("4x6", 20, "glossy", False) == 0


def test_non_matte_rate():
    # 4x6 non-member: extra = 5, glossy rate 7 -> 35
    assert extra_print_charge("4x6", 25, "glossy", False) == 35


def test_extra_exactly_50_boundary():
    # extra = 50 -> NOT > 50, so no bulk surcharge: 50 * 4 = 200
    assert extra_print_charge("4x6", 70, "matte", False) == 200


def test_bulk_matte_surcharge():
    # extra = 51, rate 4 + 2 = 6 -> 306
    assert extra_print_charge("4x6", 71, "matte", False) == 306


def test_bulk_glossy_no_canvas_surcharge():
    # extra = 60, rate 7 + 2 = 9 -> 540
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


def test_bulk_canvas_surcharge():
    # extra = 60, rate 7 + 2 + 5 = 14 -> 840
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


def test_small_canvas_no_bulk():
    # extra = 5, canvas but not bulk -> rate 7 -> 35
    assert extra_print_charge("4x6", 25, "canvas", False) == 35


# ---------- order_valid ----------
def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_order_valid():
    assert order_valid(10, 50, True) is True


def test_rush_order_too_many_copies():
    assert order_valid(10, 51, True) is False


def test_rush_ignores_file_size():
    assert order_valid(100, 10, True) is True


def test_file_too_large():
    assert order_valid(26, 100, False) is False


def test_file_exactly_25_ok():
    assert order_valid(25, 100, False) is True


def test_normal_order_max_copies():
    assert order_valid(10, 500, False) is True


def test_normal_order_too_many_copies():
    assert order_valid(10, 501, False) is False


# ---------- dispatch_status ----------
def test_dispatch_on_time_standard():
    assert dispatch_status(12, False, False) == "on_time"


def test_dispatch_tight_standard():
    assert dispatch_status(8, False, False) == "tight"


def test_dispatch_tight_lower_boundary():
    assert dispatch_status(6, False, False) == "tight"


def test_dispatch_missed_standard():
    assert dispatch_status(5, False, False) == "missed"


def test_dispatch_framed_on_time():
    assert dispatch_status(24, True, False) == "on_time"


def test_dispatch_framed_tight():
    assert dispatch_status(20, True, False) == "tight"


def test_dispatch_framed_missed():
    assert dispatch_status(10, True, False) == "missed"


def test_dispatch_international_unframed_on_time():
    assert dispatch_status(36, False, True) == "on_time"


def test_dispatch_international_framed_on_time():
    assert dispatch_status(48, True, True) == "on_time"


def test_dispatch_international_framed_missed():
    assert dispatch_status(10, True, True) == "missed"