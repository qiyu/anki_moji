import json
import os


def get_config():
    try:
        config_file = os.path.join(get_addon_dir(), 'config.json')
        with open(config_file, 'r') as f:
            config = json.loads(f.read())
        if not config:
            config = {}
    except IOError:
        config = {}
    return config


def update_config(config: dict):
    origin = get_config()
    origin.update(config)
    config_file = os.path.join(get_addon_dir(), 'config.json')
    with open(config_file, 'w') as f:
        json.dump(origin, f, sort_keys=True, indent=2)


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


def get_module_name():
    return __name__.split(".")[0]


def get_addon_dir():
    try:
        from aqt import mw
    except ModuleNotFoundError:
        return os.getcwd()

    if mw is None:
        return os.getcwd()

    root = mw.pm.addonFolder()
    addon_dir = os.path.join(root, get_module_name())
    return addon_dir


def get_link(r):
    if r.target_type == 102:
        return "https://www.mojidict.com/details/" + r.target_id
    elif r.target_type == 103:
        return "https://www.mojidict.com/example/" + r.target_id
    elif r.target_type == 120:
        return "https://www.mojidict.com/sentence/" + r.target_id
    else:
        return ''
