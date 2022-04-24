import logging
import sys

from PyQt5.QtWidgets import QApplication

from .core import common
from .core.gui import MainWindow


def main():
    common.no_anki_mode = True
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s', stream=sys.stdout)
    # 必须要将QApplication赋值到一个变量，否则会被自动回收
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec_())


if __name__ == '__main__':
    main()
