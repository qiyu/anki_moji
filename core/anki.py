import re

from anki.template import TemplateRenderContext


def on_edit_filter(text, field, filter_, context: TemplateRenderContext):
    if filter_ == 'MojiToAnki_link':
        # 将这种数据转换为http链接：<a href="https://www.mojidict.com/details/xxxx">Moji Web</a>
        match = re.fullmatch('<a href="(.+)">Moji Web</a>', text)
        if match:
            return match.group(1)
    return text
