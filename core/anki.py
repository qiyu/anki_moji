import re

from anki.collection import SearchNode
from anki.template import TemplateRenderContext

from . import common, styles
from .common import common_log


def on_field_filter(text, field, filter_, context: TemplateRenderContext):
    if filter_ == 'MojiToAnki_link':
        # 将这种数据转换为http链接：<a href="https://www.mojidict.com/details/xxxx">Moji Web</a>
        # 另外，也可以直接从note中拼接出链接
        match = re.fullmatch('<a href="(.+)">Moji Web</a>', text)
        if match:
            return match.group(1)
    return text


def get_current_review_note():
    from aqt import mw
    card = mw.reviewer.card
    if not card:
        raise Exception('只有在复习时才可以使用该功能')

    note = card.note()
    try:
        target_id = note['target_id']
        target_type = int(note['target_type'])
        title = note['title']
    except KeyError:
        raise Exception('当前数据不是从moji web中导入的，无法更新')

    if not target_id:
        raise Exception('当前数据不是从moji web中导入的，无法更新')

    return note, target_id, target_type, title


def refresh_current_note(note, word):
    from aqt import mw

    try:
        if word.examples:
            note['examples'] = word.examples
        if word.trans:
            note['trans'] = word.trans
        if word.part_of_speech:
            note['part_of_speech'] = word.part_of_speech
    except KeyError:
        raise Exception('当前笔记模板不是最新的，请先使用导入功能更新笔记模板')

    op_changes = mw.col.update_note(note)
    mw.reviewer.op_executed(op_changes, None, True)


def check_duplicate(deck_name, target_id):
    if common.no_anki_mode:
        return False

    from aqt import mw
    note_dupes = mw.col.find_notes(
        mw.col.build_search_string(target_id, SearchNode(field_name='target_id', deck=deck_name))
    )
    return len(note_dupes) > 0


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


def update_model_fields(model, collection):
    names = list(map(lambda fld: fld['name'], model['flds']))

    changed = False
    for field_name in ALL_FIELDS:
        if field_name not in names:
            field = collection.models.new_field(field_name)
            collection.models.add_field(model, field)
            changed = True
            common_log(f'增加noteType字段，field_name：{field_name}')

    if changed:
        collection.models.save(model)


OLD_TEMPLATE_NAME = 'spell -> detail'
TEMPLATE_NAME = 'AnkiToMoji v2.0.0'


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
        target['name'] = TEMPLATE_NAME
        target['qfmt'] = styles.front_spell
        target['afmt'] = styles.detail
        model['css'] = styles.model_css_class

        collection.models.save(model)
        common_log(f'更新noteType模板信息，template_name：{TEMPLATE_NAME}')

    return False


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
