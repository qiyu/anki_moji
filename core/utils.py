import os

from aqt import mw


def get_config():
    # Load config from config.json file
    # if not mw:
    #     return {}
    # config = mw.addonManager.getConfig(get_module_name())
    # if config is None:
    #     return {}
    # return config
    return {}

def update_config(config: dict):
    if not mw:
        return
    # mw.addonManager.writeConfig(get_module_name(), config)


def get(obj: dict, path: str):
    field_names = path.split('.')
    current = obj
    for field_name in field_names:
        current = current.get(field_name)
        if current is None:
            return None
    return current
