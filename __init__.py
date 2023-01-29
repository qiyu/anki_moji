from PyQt5.QtWidgets import QAction
from anki import hooks
from aqt import mw, gui_hooks

from .core import common
from .core.gui import activate_import
from .core.hooks import on_js_message, on_field_filter
from .core.mojidict_server import MojiServer

hooks.field_filter.append(on_field_filter)
gui_hooks.webview_did_receive_js_message.append(on_js_message)

moji_server = MojiServer()

common.moji_server = moji_server

import_action = QAction('从Moji导入', mw)
import_action.triggered.connect(lambda: activate_import(moji_server))
mw.form.menuTools.addAction(import_action)
