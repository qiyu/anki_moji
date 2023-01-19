from PyQt5.QtWidgets import QAction
from anki import hooks
from aqt import mw

from .core.mojidict_server import MojiServer
from .core.anki import on_field_filter
from .core.gui import activate_import

hooks.field_filter.append(on_field_filter)
moji_server = MojiServer()

import_action = QAction('从Moji导入', mw)
import_action.triggered.connect(lambda: activate_import(moji_server))
mw.form.menuTools.addAction(import_action)
