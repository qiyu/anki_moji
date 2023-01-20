def get(obj: dict, path: str):
    if obj is None:
        return None
    field_names = path.split('.')
    current = obj
    for field_name in field_names:
        current = current.get(field_name)
        if current is None:
            return None
    return current


def get_link(r):
    if r.target_type == 102:
        return "https://www.mojidict.com/details/" + r.target_id
    elif r.target_type == 103:
        return "https://www.mojidict.com/example/" + r.target_id
    elif r.target_type == 120:
        return "https://www.mojidict.com/sentence/" + r.target_id
    else:
        return ''
