from DateTime import DateTime


def format_date_time(date_time: DateTime) -> str:
    return f'{date_time.year()}-{date_time.mm()}-{date_time.dd()}'
