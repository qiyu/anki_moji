from PyQt5.QtWidgets import QAction
from aqt import mw

from .core.gui import MainWindow


def activate():
    window = MainWindow()
    window.exec_()


action = QAction('从Moji导入', mw)
action.triggered.connect(activate)
mw.form.menuTools.addAction(action)
