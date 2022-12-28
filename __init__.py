from PyQt5.QtWidgets import QAction
from anki import hooks
from aqt import mw

from .core.anki import on_edit_filter
from .core.gui import MainWindow


def activate():
    window = MainWindow()
    window.exec()


hooks.field_filter.append(on_edit_filter)

action = QAction('从Moji导入', mw)
action.triggered.connect(activate)
mw.form.menuTools.addAction(action)
