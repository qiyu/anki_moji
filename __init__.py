from PyQt5.QtWidgets import QAction
from anki import hooks
from aqt import mw

from .core.anki import on_field_filter
from .core.gui import MainWindow

hooks.field_filter.append(on_field_filter)


def activate_import():
    window = MainWindow()
    window.exec()


import_action = QAction('从Moji导入', mw)
import_action.triggered.connect(activate_import)
mw.form.menuTools.addAction(import_action)


def activate_update():
    if mw.reviewer.card:
        pass
    print()


update_action = QAction('从Moji更新', mw)
update_action.triggered.connect(activate_update)
mw.form.menuTools.addAction(update_action)
