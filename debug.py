import sys

from PyQt5.QtWidgets import QApplication

from core import common
from core.gui import activate_import
from core.mojidict_server import MojiServer


def main():
    common.no_anki_mode = True
    moji_server = MojiServer()

    # 必须要将QApplication赋值到一个变量，否则会被自动回收
    app = QApplication(sys.argv)
    activate_import(moji_server)


if __name__ == '__main__':
    main()
