import json
import os

from . import styles

from .common import common_log


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


ALL_FIELDS = ['title', 'note', 'target_id', 'target_type', 'spell', 'accent', 'pron', 'excerpt', 'sound', 'link',
              'part_of_speech', 'trans', 'examples']


def prepare_model(model_name, deck_name, collection):
    """
    Returns a model for our future notes.
    Creates a deck to keep them.
    """
    if is_model_exist(model_name, collection, ALL_FIELDS):
        model = collection.models.by_name(model_name)
    else:
        model = create_new_model(model_name, collection)
    model['did'] = collection.decks.id(deck_name)

    collection.models.set_current(model)
    collection.models.save(model)

    # 处理历史版本的模板数据
    update_template(model, collection)
    return model


def is_model_exist(model_name, collection, fields):
    all_names = [x.name for x in collection.models.all_names_and_ids()]
    name_exist = model_name in all_names
    return name_exist


OLD_TEMPLATE_NAME = 'spell -> detail'
TEMPLATE_NAME = 'spell -> detail v2.0.0'


def update_template(model, collection):
    target = None
    if len(model['tmpls']) == 1:
        target = model['tmpls'][0]
    else:
        for tmpl in model['tmpls']:
            if tmpl['name'] == OLD_TEMPLATE_NAME:
                target = tmpl

    if target is not None and target['name'] != TEMPLATE_NAME:
        target['name'] = TEMPLATE_NAME
        target['qfmt'] = styles.front_spell
        target['afmt'] = styles.detail
        model['css'] = styles.model_css_class

        collection.models.save(model)
        common_log(f'更新模板信息，name：{TEMPLATE_NAME}')


def create_new_model(model_name, collection):
    model = collection.models.new(model_name)
    model['css'] = styles.model_css_class
    for field in ALL_FIELDS:
        collection.models.addField(model, collection.models.new_field(field))

    template1 = collection.models.new_template(TEMPLATE_NAME)
    template1['qfmt'] = styles.front_spell
    template1['afmt'] = styles.detail
    collection.models.addTemplate(model, template1)

    return model


def get_link(r):
    if r.target_type == 102:
        return "https://www.mojidict.com/details/" + r.target_id
    elif r.target_type == 103:
        return "https://www.mojidict.com/example/" + r.target_id
    elif r.target_type == 120:
        return "https://www.mojidict.com/sentence/" + r.target_id
    else:
        return ''
