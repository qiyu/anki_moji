import sys
from multiprocessing.pool import ThreadPool
from core.gui import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
thread_pool = ThreadPool(1)
window = MainWindow(thread_pool)
sys.exit(window.exec_())
