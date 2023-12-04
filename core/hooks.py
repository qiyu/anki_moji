#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2023/01/20.
# Mail:qiyu.one@gmail.com
import re

from aqt import mw
from aqt.reviewer import Reviewer

from . import common
from .gui import login_if_need, UpdateWindow
from .mojidict_server import MojiServer


def on_field_filter(text, field, filter_, context):
    if filter_ == 'MojiToAnki_link':
        # 将这种数据转换为http链接：<a href="https://www.mojidict.com/details/xxxx">Moji Web</a>
        # 另外，也可以直接从note中拼接出链接
        match = re.fullmatch('<a href="(.+)">Moji Web</a>', text)
        if match:
            return match.group(1)
    return text


def on_js_message(handled, url, context):
    try:
        if url == "MojiToAnki_update":
            if not isinstance(context, Reviewer):
                return handled
            card = context.card
            note = card.note()
            moji_server: MojiServer = common.moji_server
            login_if_need(moji_server, parent=mw)
            window = UpdateWindow(mw, moji_server, note)
            window.exec()

            if window.op_changes:
                context.op_executed(window.op_changes, None, True)
            return True, None
    except Exception:
        common.get_logger().exception('on_js_message failed')
        return True, None

    return handled
