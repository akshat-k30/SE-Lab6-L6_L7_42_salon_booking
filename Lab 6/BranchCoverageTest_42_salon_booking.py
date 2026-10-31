import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# ───────────────────────────────────────────────
# Branch Coverage Tests for extra_time_charge
# ───────────────────────────────────────────────
# Branches to cover:
#   B1: service not in INCLUDED_MIN → True / False
#   B2: duration_min < 0 → True / False
#   B3: is_member and service != "spa" → True / False (member+spa, member+non-spa, non-member)
#   B4: extra <= 0 → True / False
#   B5: stylist_level == "junior" → True / False
#   B6: extra > 60 → True / False
#   B7: stylist_level == "senior" (inside extra>60) → True / False

def test_etc_unknown_service():
    """B1-True: unknown service raises ValueError."""
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("nails", 20, "junior", False)

def test_etc_negative_duration():
    """B2-True: negative duration raises ValueError."""
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)

def test_etc_no_extra_non_member():
    """B4-True: duration within included time, non-member."""
    # haircut included=30, duration=25 → extra = -5 ≤ 0 → return 0
    assert extra_time_charge("haircut", 25, "junior", False) == 0

def test_etc_member_non_spa_within_included():
    """B3-True (is_member=True, service≠spa): member gets +15 included.
       B4-True: still within included → return 0."""
    # haircut included = 30+15 = 45, duration 40 → extra = -5
    assert extra_time_charge("haircut", 40, "junior", True) == 0

def test_etc_member_spa_no_bonus():
    """B3-False path (service == 'spa'): member does NOT get +15 for spa.
       Extra = 100 - 90 = 10, junior rate = 10."""
    assert extra_time_charge("spa", 100, "junior", True) == 100

def test_etc_non_member_extra_junior():
    """B3-False (non-member), B5-True (junior), B6-False (extra ≤ 60).
       haircut: 30 included, 50 duration → extra=20, rate=10 → 200."""
    assert extra_time_charge("haircut", 50, "junior", False) == 200

def test_etc_non_member_extra_senior_small():
    """B5-False (senior), B6-False (extra ≤ 60).
       haircut: 30 included, 50 duration → extra=20, rate=18 → 360."""
    assert extra_time_charge("haircut", 50, "senior", False) == 360

def test_etc_over60_junior():
    """B6-True, B7-False (junior): rate = 10+8 = 18.
       colour: 60 included, 130 duration → extra=70 → 70*18 = 1260."""
    assert extra_time_charge("colour", 130, "junior", False) == 1260

def test_etc_over60_senior():
    """B6-True, B7-True (senior): rate = 18+8+4 = 30.
       colour: 60 included, 130 duration → extra=70 → 70*30 = 2100."""
    assert extra_time_charge("colour", 130, "senior", False) == 2100

def test_etc_exact_boundary_extra_zero():
    """B4-True boundary: extra = 0 exactly → return 0."""
    assert extra_time_charge("haircut", 30, "junior", False) == 0

def test_etc_exact_boundary_extra_one():
    """B4-False boundary: extra = 1 → junior rate 10 → 10."""
    assert extra_time_charge("haircut", 31, "junior", False) == 10

def test_etc_exact_boundary_extra_60():
    """B6-False boundary: extra = 60 (not > 60) → rate stays base."""
    # haircut included=30, duration=90 → extra=60, senior rate=18 → 1080
    assert extra_time_charge("haircut", 90, "senior", False) == 1080

def test_etc_exact_boundary_extra_61():
    """B6-True boundary: extra = 61, junior → rate=10+8=18 → 61*18 = 1098."""
    assert extra_time_charge("haircut", 91, "junior", False) == 1098

def test_etc_colour_service():
    """Verifies colour included=60 works correctly."""
    assert extra_time_charge("colour", 60, "junior", False) == 0

def test_etc_spa_service():
    """Verifies spa included=90 works correctly."""
    assert extra_time_charge("spa", 90, "senior", False) == 0


# ───────────────────────────────────────────────
# Branch Coverage Tests for can_book
# ───────────────────────────────────────────────
# Branches:
#   B1: is_walk_in → True / False
#   B2: (walk-in) party_size <= 2 → True / False
#   B3: party_size > 4 → True / False
#   B4: services <= 2 → True / False

def test_cb_walkin_party2():
    """B1-True, B2-True: walk-in, party ≤ 2 → True."""
    assert can_book(2, 1, True) is True

def test_cb_walkin_party1():
    """B1-True, B2-True: walk-in, party = 1 → True."""
    assert can_book(1, 1, True) is True

def test_cb_walkin_party3():
    """B1-True, B2-False: walk-in, party > 2 → False."""
    assert can_book(3, 1, True) is False

def test_cb_reservation_party5():
    """B1-False, B3-True: reservation, party > 4 → False."""
    assert can_book(5, 1, False) is False

def test_cb_reservation_party4_services2():
    """B1-False, B3-False, B4-True: party ≤ 4, services ≤ 2 → True."""
    assert can_book(4, 2, False) is True

def test_cb_reservation_party3_services3():
    """B1-False, B3-False, B4-False: party ≤ 4, services > 2 → False."""
    assert can_book(3, 3, False) is False

def test_cb_reservation_party1_services1():
    """B1-False, B3-False, B4-True: small party reservation → True."""
    assert can_book(1, 1, False) is True


# ───────────────────────────────────────────────
# Branch Coverage Tests for arrival_status
# ───────────────────────────────────────────────
# Branches:
#   B1: is_colour → True / False (cutoff = 10 vs 5)
#   B2: is_weekend → True / False (cutoff += 10)
#   B3: minutes_early >= cutoff → "open"
#   B4: minutes_early >= cutoff - 15 → "late"
#   B5: else → "closed"

def test_as_not_colour_not_weekend_open():
    """B1-False, B2-False: cutoff=5. minutes=5 → 'open'."""
    assert arrival_status(5, False, False) == "open"

def test_as_not_colour_not_weekend_late():
    """B1-False, B2-False: cutoff=5, cutoff-15=-10. minutes=0 → 'late'."""
    assert arrival_status(0, False, False) == "late"

def test_as_colour_not_weekend_open():
    """B1-True, B2-False: cutoff=10. minutes=10 → 'open'."""
    assert arrival_status(10, True, False) == "open"

def test_as_colour_not_weekend_late():
    """B1-True, B2-False: cutoff=10, cutoff-15=-5. minutes=5 → 'late'."""
    assert arrival_status(5, True, False) == "late"

def test_as_not_colour_weekend_open():
    """B1-False, B2-True: cutoff=5+10=15. minutes=15 → 'open'."""
    assert arrival_status(15, False, True) == "open"

def test_as_not_colour_weekend_late():
    """B1-False, B2-True: cutoff=15, cutoff-15=0. minutes=5 → 'late'."""
    assert arrival_status(5, False, True) == "late"

def test_as_colour_weekend_open():
    """B1-True, B2-True: cutoff=10+10=20. minutes=20 → 'open'."""
    assert arrival_status(20, True, True) == "open"

def test_as_colour_weekend_late():
    """B1-True, B2-True: cutoff=20, cutoff-15=5. minutes=6 → 'late'."""
    assert arrival_status(6, True, True) == "late"

def test_as_colour_weekend_closed():
    """B1-True, B2-True: cutoff=20, cutoff-15=5. minutes=4 → 'closed'."""
    assert arrival_status(4, True, True) == "closed"

def test_as_not_colour_not_weekend_closed():
    """B1-False, B2-False: cutoff=5, cutoff-15=-10. minutes=-11 → 'closed'."""
    assert arrival_status(-11, False, False) == "closed"

