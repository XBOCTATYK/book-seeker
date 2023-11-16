def safe_parse_to_float(number):
    if number is None:
        return 0

    try:
        return float(number)
    except ValueError:
        return 0
