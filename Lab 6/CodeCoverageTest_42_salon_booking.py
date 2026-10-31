import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# ───────────────────────────────────────────────
# Tests for extra_time_charge
# ───────────────────────────────────────────────

def test_extra_time_unknown_service():
    """Service not in INCLUDED_MIN raises ValueError."""
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("perm", 30, "junior", False)

def test_extra_time_negative_duration():
    """Negative duration raises ValueError."""
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)

def test_extra_time_within_included():
    """Duration within included minutes returns 0."""
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_extra_time_member_bonus_haircut():
    """Member gets +15 included minutes for haircut (not spa)."""
    # haircut included = 30 + 15 = 45 for member, duration 40 => extra <= 0
    assert extra_time_charge("haircut", 40, "junior", True) == 0

def test_extra_time_member_spa_no_bonus():
    """Member does NOT get +15 for spa service."""
    # spa included = 90, duration 100 => extra = 10, junior rate = 10
    assert extra_time_charge("spa", 100, "junior", True) == 10 * 10

def test_extra_time_junior_rate():
    """Junior stylist: rate = 10 per extra minute."""
    # haircut included = 30, duration 50 => extra = 20
    assert extra_time_charge("haircut", 50, "junior", False) == 20 * 10

def test_extra_time_senior_rate():
    """Non-junior (senior) stylist: rate = 18 per extra minute."""
    # haircut included = 30, duration 50 => extra = 20
    assert extra_time_charge("haircut", 50, "senior", False) == 20 * 18

def test_extra_time_over_60_junior():
    """Extra > 60 with junior: rate = 10 + 8 = 18."""
    # colour included = 60, duration 130 => extra = 70
    assert extra_time_charge("colour", 130, "junior", False) == 70 * 18

def test_extra_time_over_60_senior():
    """Extra > 60 with senior: rate = 18 + 8 + 4 = 30."""
    # colour included = 60, duration 130 => extra = 70
    assert extra_time_charge("colour", 130, "senior", False) == 70 * 30


# ───────────────────────────────────────────────
# Tests for can_book
# ───────────────────────────────────────────────

def test_can_book_walk_in_small():
    """Walk-in with party_size <= 2 returns True."""
    assert can_book(2, 1, True) is True

def test_can_book_walk_in_large():
    """Walk-in with party_size > 2 returns False."""
    assert can_book(3, 1, True) is False

def test_can_book_reservation_too_large():
    """Reservation with party_size > 4 returns False."""
    assert can_book(5, 1, False) is False

def test_can_book_reservation_ok():
    """Reservation with party_size <= 4 and services <= 2 returns True."""
    assert can_book(4, 2, False) is True

def test_can_book_reservation_too_many_services():
    """Reservation with services > 2 returns False."""
    assert can_book(3, 3, False) is False


# ───────────────────────────────────────────────
# Tests for arrival_status
# ───────────────────────────────────────────────

def test_arrival_open():
    """Arrives early enough → 'open'."""
    # not colour, not weekend => cutoff = 5; minutes_early = 5 >= 5
    assert arrival_status(5, False, False) == "open"

def test_arrival_late():
    """Arrives a bit late → 'late'."""
    # not colour, not weekend => cutoff = 5; cutoff-15 = -10; 0 >= -10 True
    assert arrival_status(0, False, False) == "late"

def test_arrival_closed():
    """Arrives far too late → 'closed'."""
    # colour, weekend => cutoff = 10+10 = 20; cutoff-15 = 5; -1 < 5
    assert arrival_status(-1, True, True) == "closed"

def test_arrival_colour_open():
    """Colour appointment, early enough → 'open'."""
    # colour => cutoff = 10; minutes_early = 10 >= 10
    assert arrival_status(10, True, False) == "open"

def test_arrival_weekend_open():
    """Weekend adds 10 to cutoff; still 'open'."""
    # not colour, weekend => cutoff = 5+10 = 15; 15 >= 15
    assert arrival_status(15, False, True) == "open"

