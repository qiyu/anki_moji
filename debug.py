import sys

from PyQt5.QtWidgets import QApplication

from core.gui import MainWindow


def main():
    # 必须要将QApplication赋值到一个变量，否则会被自动回收
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec_())


if __name__ == '__main__':
    main()
