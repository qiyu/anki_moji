import json
import os

from . import styles
from .mojidict_server import MojiWord


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


fields = ['title', 'note', 'target_id', 'target_type', 'spell', 'accent', 'pron', 'excerpt', 'sound', 'link',
          'part_of_speech', 'trans', 'examples']


def prepare_model(model_name, deck_name, collection):
    """
    Returns a model for our future notes.
    Creates a deck to keep them.
    """
    if is_model_exist(model_name, collection, fields):
        model = collection.models.by_name(model_name)
    else:
        model = create_new_model(model_name, collection)
    # Create a deck "LinguaLeo" and write id to deck_id
    model['did'] = collection.decks.id(deck_name)
    collection.models.set_current(model)
    collection.models.save(model)
    return model


def is_model_exist(model_name, collection, fields):
    all_names = [x.name for x in collection.models.all_names_and_ids()]
    name_exist = model_name in all_names
    return name_exist


def create_new_model(model_name, collection):
    model = collection.models.new(model_name)
    model['css'] = styles.model_css_class
    for field in fields:
        collection.models.addField(model, collection.models.new_field(field))

    template1 = collection.models.new_template('spell -> detail')
    template1['qfmt'] = styles.front_spell
    template1['afmt'] = styles.detail
    collection.models.addTemplate(model, template1)

    template2 = collection.models.new_template('pron -> detail')
    template2['qfmt'] = styles.front_pron
    template2['afmt'] = styles.detail
    collection.models.addTemplate(model, template2)

    template3 = collection.models.new_template('trans -> detail')
    template3['qfmt'] = styles.front_trans
    template3['afmt'] = styles.detail
    collection.models.addTemplate(model, template3)

    return model


def get_link(r: MojiWord):
    if r.target_type == 102:
        return "https://www.mojidict.com/details/" + r.target_id
    elif r.target_type == 103:
        return "https://www.mojidict.com/example/" + r.target_id
    elif r.target_type == 120:
        return "https://www.mojidict.com/sentence/" + r.target_id
    else:
        return ''
