import json
import os

from aqt import mw

from . import styles

MODEL_NAME = 'MOJITEST_MODEL'
DECK_NAME = 'MOJITEST_DECK'


def get_config():
    try:
        config_file = os.path.join(get_addon_dir(), 'config.json')
        with open(config_file, 'r') as f:
            config = json.loads(f.read())
    except IOError:
        config = {}
    return config


def update_config(config: dict):
    config_file = os.path.join(get_addon_dir(), 'config.json')
    with open(config_file, 'w') as f:
        json.dump(config, f, sort_keys=True, indent=2)


def get(obj: dict, path: str):
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
    if mw is None:
        return os.getcwd()
    root = mw.pm.addonFolder()
    addon_dir = os.path.join(root, get_module_name())
    return addon_dir


fields = ['target_id', 'target_type', 'title', 'spell', 'accent', 'pron', 'excerpt', 'sound', 'link', 'note']


def prepare_model(collection):
    """
    Returns a model for our future notes.
    Creates a deck to keep them.
    """
    if is_model_exist(collection, fields):
        model = collection.models.byName(MODEL_NAME)
    else:
        model = create_new_model(collection)
    # Create a deck "LinguaLeo" and write id to deck_id
    model['did'] = collection.decks.id(DECK_NAME)
    collection.models.setCurrent(model)
    collection.models.save(model)
    return model


def is_model_exist(collection, fields):
    name_exist = MODEL_NAME in collection.models.allNames()
    if name_exist:
        fields_ok = collection.models.fieldNames(collection.models.byName(
            MODEL_NAME)) == fields
    else:
        fields_ok = False
    return name_exist and fields_ok


def create_new_model(collection):
    model = collection.models.new(MODEL_NAME)
    model['css'] = styles.model_css_class
    for field in fields:
        collection.models.addField(model, collection.models.newField(field))
    template = create_templates(collection)
    collection.models.addTemplate(model, template)
    # todo 验证是否可以不设置id
    # model['id'] = randint(100000, 1000000)  # Essential for upgrade detection
    collection.models.update(model)
    return model


def create_templates(collection):
    template = collection.models.newTemplate('spell -> detail')
    template['qfmt'] = styles.question
    template['afmt'] = styles.answer
    return template
