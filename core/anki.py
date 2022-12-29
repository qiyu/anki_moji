import re

from anki.collection import SearchNode
from anki.template import TemplateRenderContext

from . import common


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
