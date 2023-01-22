#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2023/01/20.
# Mail:qiyu.one@gmail.com
import traceback

from aqt import mw
from aqt.reviewer import Reviewer

from . import common
from .common import common_log
from .gui import login_if_need, UpdateWindow
from .mojidict_server import MojiServer


def on_js_message(handled, url, context):
    try:
        if url == "MojiToAnki_update":
            if not isinstance(context, Reviewer):
                return handled
            card = context.card
            note = card.note()
            moji_server: MojiServer = common.moji_server
            login_if_need(moji_server)
            window = UpdateWindow(mw, moji_server, note)
            window.exec()

            if window.op_changes:
                context.op_executed(window.op_changes, None, True)
            return True, None
    except:
        common_log('on_js_message failed:' + traceback.format_exc())
        return True, None

    return handled
