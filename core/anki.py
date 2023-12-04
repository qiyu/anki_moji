import json
import os
import shutil

from . import styles, common
from aqt import mw

_MEDIA_FILES_ICONFONT = '_iconfont.7a6f8a1.ttf'


def check_duplicate(deck_name, target_id):
    note_dupes = mw.col.find_notes(f'deck:"{deck_name}" and target_id:"{target_id}"')
    # 直接返回note数组便于可能的update操作，同时可作为bool与之前的定义兼容
    return [mw.col.get_note(note_id) for note_id in note_dupes]


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
    return model


def is_model_exist(model_name, collection, fields):
    all_names = [x.name for x in collection.models.all_names_and_ids()]
    name_exist = model_name in all_names
    return name_exist


def update_model_fields(model, collection, force=False) -> bool:
    names = list(map(lambda fld: fld['name'], model['flds']))

    changed = False
    for field_name in ALL_FIELDS:
        if field_name not in names:
            if not force:
                # 返回True表示需要询问用户
                return True
            field = collection.models.new_field(field_name)
            collection.models.add_field(model, field)
            changed = True
            common.get_logger().info(f'add field to noteType, field_name: {field_name}')

    if changed:
        collection.models.save(model)
    return False


OLD_TEMPLATE_NAME = 'AnkiToMoji v2.0.0'
TEMPLATE_NAME = 'MojiToAnki 3'


def update_template(model, collection, force=False) -> bool:
    target = None
    if len(model['tmpls']) == 1:
        target = model['tmpls'][0]
    else:
        for tmpl in model['tmpls']:
            if tmpl['name'] == OLD_TEMPLATE_NAME:
                target = tmpl

    if target is not None and target['name'] != TEMPLATE_NAME:
        if not force:
            # 返回True表示需要询问用户
            return True

        _prepare_media_files(_MEDIA_FILES_ICONFONT)
        target['name'] = TEMPLATE_NAME
        target['qfmt'] = styles.front_spell
        target['afmt'] = styles.detail
        model['css'] = styles.model_css_class

        collection.models.save(model)
        common.get_logger().info(f'update template, template_name: {TEMPLATE_NAME}')

    return False


def create_new_model(model_name, collection):
    _prepare_media_files(_MEDIA_FILES_ICONFONT)

    model = collection.models.new(model_name)
    model['css'] = styles.model_css_class
    for field in ALL_FIELDS:
        collection.models.addField(model, collection.models.new_field(field))

    template1 = collection.models.new_template(TEMPLATE_NAME)
    template1['qfmt'] = styles.front_spell
    template1['afmt'] = styles.detail
    collection.models.addTemplate(model, template1)

    return model


def _prepare_media_files(file):
    from aqt import mw
    target_path = os.path.join(mw.col.media.dir(), file)
    if not os.path.lexists(target_path):
        source_path = os.path.join(get_addon_dir(), 'assets', file)
        shutil.copyfile(source_path, target_path)
        common.get_logger().info(f'copy file: {file}')


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


def _get_module_name():
    return __name__.split(".")[0]


def get_addon_dir():
    try:
        from aqt import mw
    except ModuleNotFoundError:
        return os.getcwd()

    if mw is None:
        return os.getcwd()

    root = mw.pm.addonFolder()
    addon_dir = os.path.join(root, _get_module_name())
    return addon_dir
