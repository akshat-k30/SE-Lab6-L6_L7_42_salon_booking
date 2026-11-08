from hypothesis import given, strategies as st, settings
from salon_booking import parse_booking, duration_average, payable_bill


# ───────────────────────────────────────────────
# Fuzz Tests for parse_booking
# ───────────────────────────────────────────────

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    """Fuzz parse_booking: it must never crash on any input.
    Instead of raising unhandled exceptions, it should return a
    tuple (str, float) for valid inputs or raise a ValueError
    for invalid ones."""
    try:
        result = parse_booking(s)
        # If it returns, it must be a tuple of (str, float)
        assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
        assert len(result) == 2, f"Expected 2 elements, got {len(result)}"
        assert isinstance(result[0], str), f"Service should be str, got {type(result[0])}"
        assert isinstance(result[1], float), f"Duration should be float, got {type(result[1])}"
    except ValueError:
        pass  # ValueError is acceptable for invalid input
    except TypeError:
        assert False, f"parse_booking crashed with TypeError on input: {s!r}"
    except Exception as e:
        assert False, f"parse_booking crashed with {type(e).__name__}: {e} on input: {s!r}"


# ───────────────────────────────────────────────
# Fuzz Tests for duration_average
# ───────────────────────────────────────────────

@given(st.text() | st.none())
def test_duration_average_no_crash(s):
    """Fuzz duration_average: it must never crash on any input.
    Should return an int for valid CSV of integers, or raise ValueError
    for invalid inputs."""
    try:
        result = duration_average(s)
        # If it returns, the result should be a numeric type
        assert isinstance(result, (int, float)), (
            f"Expected numeric result, got {type(result)}"
        )
    except ValueError:
        pass  # ValueError is acceptable for invalid input
    except ZeroDivisionError:
        assert False, f"duration_average crashed with ZeroDivisionError on input: {s!r}"
    except TypeError:
        assert False, f"duration_average crashed with TypeError on input: {s!r}"
    except Exception as e:
        assert False, f"duration_average crashed with {type(e).__name__}: {e} on input: {s!r}"


# ───────────────────────────────────────────────
# Fuzz Tests for payable_bill
# ───────────────────────────────────────────────

@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    """Fuzz payable_bill: it must never crash on any input.
    Should return a float >= 0 for valid inputs, or raise ValueError
    for invalid ones."""
    try:
        result = payable_bill(s)
        # If it returns, the result should be a non-negative number
        assert isinstance(result, (int, float)), (
            f"Expected numeric result, got {type(result)}"
        )
        assert result >= 0, f"Payable bill should be non-negative, got {result}"
    except ValueError:
        pass  # ValueError is acceptable for invalid input
    except TypeError:
        assert False, f"payable_bill crashed with TypeError on input: {s!r}"
    except Exception as e:
        assert False, f"payable_bill crashed with {type(e).__name__}: {e} on input: {s!r}"

