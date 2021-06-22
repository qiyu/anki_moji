# This Python file uses the following encoding: utf-8
import datetime
import os
import sys
from functools import lru_cache
from multiprocessing.pool import ThreadPool
from typing import Optional

from PySide2.QtCore import QFile, Slot, Qt, QUrl
from PySide2.QtGui import QKeyEvent, QDesktopServices
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget
from playsound import playsound
from pydash import map_, filter_

from mojidicttool import mojidict_server, storage, dao
from mojidicttool.model import Word

TTS_DIR_PATH = '/Users/qiyu/Library/ApplicationSupport/Anki2/qiyu/collection.media'
_thread_pool = ThreadPool(1)


class MojiDictTool(QWidget):
    def __init__(self):
        super(MojiDictTool, self).__init__()
        self.words = []
        self.index = 0
        self.inited = False

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    @lru_cache()
    def find(self, name):
        return self.findChild(QWidget, name)

    def init(self):
        self.load_ui()
        self.connect_ui()
        self.start_show()

    @property
    def current_word(self) -> Optional[Word]:
        try:
            return self.words[self.index]
        except IndexError:
            return None

    def refresh_mojiwords(self):
        new_mojiwords = mojidict_server.fetch_all_from_server()
        old_mojiwords = dao.query_all()
        old_target_ids = map_(old_mojiwords, 'target_id')
        new_target_ids = map_(new_mojiwords, 'target_id')
        for item in new_mojiwords:
            if item.target_id not in old_target_ids:
                dao.insert(item)
        for item in old_mojiwords:
            if item.target_id not in new_target_ids:
                dao.delete(item.target_id)

    def start_show(self):
        self.words = filter_(dao.query_all(),
                             lambda x: x.next_review_time is None or x.next_review_time < datetime.datetime.now())
        self.inited = True
        self.index = 0
        self.show_new_word()

    def connect_ui(self):
        self.find('button_remembered').clicked.connect(lambda: self.button_remembered())
        self.find('button_unremembered').clicked.connect(lambda: self.button_unremembered())
        self.find('button_show_detail').clicked.connect(lambda: self.button_show_detail())
        self.find('button_read').clicked.connect(lambda: self.button_read())
        self.find('button_moji').clicked.connect(lambda: self.button_moji())
        self.find('button_sync').clicked.connect(lambda: self.button_sync())

    @Slot()
    def button_moji(self):
        if not self.current_word:
            return

        QDesktopServices.openUrl(QUrl(f'https://www.mojidict.com/details/{self.current_word.target_id}'))

    @Slot()
    def button_sync(self):
        self.refresh_mojiwords()
        self.start_show()

    @Slot()
    def button_remembered(self):
        if not self.current_word:
            return

        dao.review_word(self.current_word, reset=False)
        if self.index == len(self.words):
            return
        self.index += 1

        self.show_new_word()

    @Slot()
    def button_unremembered(self):
        if not self.current_word:
            return

        dao.review_word(self.current_word, reset=True)
        if self.index == len(self.words):
            return
        self.words.append(self.words.pop(self.index))
        self.show_new_word()

    @Slot()
    def button_show_detail(self):
        if not self.current_word:
            return

        self.find('label_word_detail').setText('\n\n'.join(
            [self.current_word.pron + self.current_word.accent, self.current_word.excerpt]))
        self.button_read()

    @Slot()
    def button_read(self):
        if not self.current_word:
            return

        file_path = os.path.join(TTS_DIR_PATH, self.current_word.target_id + '.mp3')
        if not os.path.lexists(file_path):
            tts_url = mojidict_server.get_tts(self.current_word.target_id, self.current_word.target_type)
            storage.save_tts_file(file_path, tts_url)
        _thread_pool.apply_async(lambda: playsound(file_path))

    def show_new_word(self):
        if self.current_word:
            self.find('label_word_title').setText(self.current_word.title)
            self.find('label_count').setText(f'{self.index}/{len(self.words)}')
        else:
            self.find('label_word_title').setText('')
            self.find('label_count').setText('')

        self.find('label_word_detail').setText('')

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Space:
            self.button_show_detail()
        elif event.key() == Qt.Key_Left:
            self.button_remembered()
        elif event.key() == Qt.Key_Right:
            self.button_unremembered()
        elif event.key() == Qt.Key_S:
            self.button_sync()
        elif event.key() == Qt.Key_M:
            self.button_moji()
        elif event.key() == Qt.Key_R:
            self.button_read()


def main():
    app = QApplication([])
    widget = MojiDictTool()
    widget.init()
    widget.show()
    sys.exit(app.exec_())


def download_all():
    new_mojiwords = mojidict_server.fetch_all_from_server()
    for r in new_mojiwords:
        file_path = os.path.join(TTS_DIR_PATH, 'moji_' + r.target_id + '.mp3')
        if not os.path.lexists(file_path):
            tts_url = mojidict_server.get_tts(r.target_id, r.target_type)
            storage.save_tts_file(file_path, tts_url)
        if r.accent is None:
            r.accent = ''
    with open('/Users/qiyu/Downloads/moji.txt', 'w') as f:
        f.write('\n'.join(
            [format_row(r)
             for r in
             new_mojiwords]))


def format_row(r):
    try:
        return '\t'.join([r.target_id, str(r.target_type),
                          r.title, r.spell, r.accent, r.pron, r.excerpt,
                          f'[sound:moji_{r.target_id}.mp3]',
                          f'<a href="https://www.mojidict.com/details/{r.target_id}">Moji Web</a>'])
    except Exception:
        print("处理异常", r.spell)
        raise


if __name__ == "__main__":
    download_all()
