import math


def parse_booking(text):
    """Parse a 'service:duration' string into (service_name, duration_float).

    Raises ValueError for any invalid input (None, missing ':', non-numeric
    duration, empty service name, negative duration, or non-finite values).
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    if ':' not in text:
        raise ValueError("Input must contain a ':' separator")
    parts = text.split(':', 1)
    service = parts[0].strip()
    minutes_str = parts[1].strip()
    if not service:
        raise ValueError("Service name cannot be empty")
    if not minutes_str:
        raise ValueError("Duration cannot be empty")
    try:
        minutes = float(minutes_str)
    except ValueError:
        raise ValueError(f"Duration must be a number, got '{minutes_str}'")
    if not math.isfinite(minutes):
        raise ValueError("Duration must be a finite number")
    if minutes < 0:
        raise ValueError("Duration cannot be negative")
    return service.title(), minutes


def duration_average(durations_csv):
    """Compute the integer average of a comma-separated list of integer durations.

    Raises ValueError for None, empty string, non-integer values, empty
    elements in the CSV, or negative durations.
    """
    if not isinstance(durations_csv, str):
        raise ValueError("Input must be a string")
    durations_csv = durations_csv.strip()
    if not durations_csv:
        raise ValueError("Input cannot be empty")
    parts = durations_csv.split(',')
    values = []
    for part in parts:
        part = part.strip()
        if not part:
            raise ValueError("Empty value found in CSV")
        try:
            val = int(part)
        except ValueError:
            raise ValueError(f"Non-integer value found: '{part}'")
        if val < 0:
            raise ValueError(f"Duration cannot be negative: {val}")
        values.append(val)
    if len(values) == 0:
        raise ValueError("No values to average")
    return sum(values) // len(values)


def payable_bill(text):
    """Compute the payable bill from a 'bill|discount' string.

    Returns max(bill * 1.18 - discount, 0).
    Raises ValueError for None, missing '|', non-numeric, non-finite, or
    negative values.
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    if '|' not in text:
        raise ValueError("Input must contain a '|' separator")
    parts = text.split('|', 1)
    bill_str = parts[0].strip()
    discount_str = parts[1].strip()
    if not bill_str:
        raise ValueError("Bill amount cannot be empty")
    if not discount_str:
        raise ValueError("Discount cannot be empty")
    try:
        bill = float(bill_str)
    except ValueError:
        raise ValueError(f"Bill must be a number, got '{bill_str}'")
    if not math.isfinite(bill):
        raise ValueError("Bill must be a finite number")
    try:
        discount = float(discount_str)
    except ValueError:
        raise ValueError(f"Discount must be a number, got '{discount_str}'")
    if not math.isfinite(discount):
        raise ValueError("Discount must be a finite number")
    if bill < 0:
        raise ValueError("Bill cannot be negative")
    if discount < 0:
        raise ValueError("Discount cannot be negative")
    total = bill * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    try:
        result = parse_booking(user_input)
        print("Service and Duration:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    try:
        result = duration_average(user_input)
        print("Average Duration:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    try:
        result = payable_bill(user_input)
        print("Payable Bill:", result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
