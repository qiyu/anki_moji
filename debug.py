import sys

from PyQt5.QtWidgets import QApplication

from core import utils
from core.gui import MainWindow


def a():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec_())

def b():
    utils.prepare_model()