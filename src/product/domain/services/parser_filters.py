def parser_filters(filters):
    pagination_name = ["limit", "page"]

    filter_clauses = []
    values = []
    values_int = []
    category = ''

    for k, v in filters.items():
        att = k[:4]
        if k not in pagination_name and att == "att_":
            filter_clauses.append(int(k[4:]))
            if v.isdigit():
                values_int.append(int(v))
            elif not v:
                continue
            else:
                values.append(v)
        elif k == 'category':
            category = v

    filter_clauses = tuple(filter_clauses)
    values = tuple(values) if values else ('',)
    values_int = tuple(values_int) if values_int else (0,)
    return filter_clauses, values, values_int, category
