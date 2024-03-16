def return_limit_and_offset(limit, offset):
    limit = limit or 10
    offset = int(offset) - 1 if offset and offset.isdigit() else 0
    return limit, offset
