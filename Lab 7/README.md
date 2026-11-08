# L6_L7_42 — Salon Booking

## Lab 7: Fuzz Testing with Hypothesis

### About

This lab explores **fuzz testing** as a security and quality assurance technique. We use the **Hypothesis** property-based fuzzing library to identify and fix input validation bugs in a salon booking Python module.

### Files

| File | Description |
|------|-------------|
| `salon_booking.py` | **Fixed** application script with robust input validation |
| `salon_booking_buggy.py` | Original **buggy** application script (before fixes) |
| `test_salon_booking.py` | Hypothesis fuzz test suite for all three functions |

### Functions Under Test

1. **`parse_booking(text)`** — Parses a `"service:duration"` string into a `(service_name, duration)` tuple
2. **`duration_average(durations_csv)`** — Computes the average of comma-separated integer durations
3. **`payable_bill(text)`** — Calculates the payable bill from a `"bill|discount"` string with 18% tax

### Bugs Found via Fuzzing

| Function | Bug | Input That Triggers It |
|----------|-----|----------------------|
| `parse_booking` | `AttributeError` — no null check | `None` |
| `parse_booking` | `ValueError` — no delimiter check | `"haircut"` (no `:`) |
| `parse_booking` | `ValueError` — non-numeric duration | `"haircut:abc"` |
| `duration_average` | `AttributeError` — no null check | `None` |
| `duration_average` | `ZeroDivisionError` — empty string | `""` |
| `duration_average` | `ValueError` — empty CSV element | `"30,,60"` |
| `duration_average` | `ValueError` — non-integer value | `"30,abc,60"` |
| `payable_bill` | `AttributeError` — no null check | `None` |
| `payable_bill` | `ValueError` — no delimiter check | `"800"` (no `|`) |
| `payable_bill` | `ValueError` — non-numeric values | `"abc|100"` |

### Fixes Applied

All three functions were hardened with:
- **Type checking** — reject `None` and non-string inputs
- **Delimiter validation** — check for required separators (`:`, `,`, `|`)
- **Empty value detection** — reject empty fields after splitting
- **Numeric parsing guards** — catch `ValueError` from `int()`/`float()`
- **Range validation** — reject negative durations and bills

### How to Run

```bash
# Install dependencies
pip install hypothesis pytest

# Run the buggy version (to see crashes)
python salon_booking_buggy.py

# Run fuzz tests (against the fixed version)
pytest test_salon_booking.py -v

# Run the fixed version
python salon_booking.py
```
