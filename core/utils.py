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


