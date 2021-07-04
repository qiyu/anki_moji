#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:yu.qi@qunar.com
from PyQt5.QtCore import QThreadPool, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit
from anki import notes
from aqt import mw

from . import utils, storage
from .mojidict_server import MojiServer


class MainWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.moji_server = MojiServer()

        self.login_field = QLineEdit()
        self.pass_field = QLineEdit()
        self.login_button = QPushButton("登录")

        self.init_window()
        self.show()

    def init_window(self):
        self.setWindowTitle('从Moji导入')
        login_label = QLabel('用户:')
        pass_label = QLabel('密码:')
        self.pass_field.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login_button_clicked)
        config = utils.get_config()
        self.login_field.setText(config.get('username', ''))
        self.pass_field.setText(config.get('password', ''))
        self.login_field.setMinimumWidth(200)
        self.pass_field.setMinimumWidth(200)
        login_form = QFormLayout()
        login_form.addRow(login_label, self.login_field)
        login_form.addRow(pass_label, self.pass_field)
        login_buttons = QHBoxLayout()
        login_buttons.addWidget(self.login_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(login_form)
        main_layout.addLayout(login_buttons)
        self.setLayout(main_layout)

    def login_button_clicked(self):
        utils.update_config({'username': self.login_field.text(), 'password': self.pass_field.text()})
        self.moji_server.login(self.login_field.text(), self.pass_field.text())
        window = ImportWindow(self.moji_server)
        window.exec_()


class ImportWindow(QDialog):
    busy_signal = pyqtSignal(bool)
    log_signal = pyqtSignal(str)

    def __init__(self, moji_server, parent=None):
        QDialog.__init__(self, parent)
        self.moji_server: MojiServer = moji_server
        self.import_button = QPushButton('导入')
        self.log_text = QPlainTextEdit()
        self.thread_pool = QThreadPool(self)
        self.thread_pool.setMaxThreadCount(1)
        self.busy_signal.connect(self.change_busy)
        self.log_signal.connect(self.add_log)
        self.init_window()
        self.show()

    def init_window(self):
        self.setWindowTitle('从Moji导入')
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumWidth(400)
        self.import_button.clicked.connect(self.import_button_clicked)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.import_button)
        main_layout.addWidget(self.log_text)
        self.setLayout(main_layout)

    @pyqtSlot(bool)
    def change_busy(self, value):
        self.import_button.setDisabled(value)

    @pyqtSlot(str)
    def add_log(self, value):
        if value:
            self.log_text.appendPlainText(value)
        else:
            self.log_text.clear()

    def import_button_clicked(self):
        self.thread_pool.start(WordLoader(self.moji_server, self.busy_signal, self.log_signal))


class WordLoader(QRunnable):
    def __init__(self, moji_server, busy_signal, log_signal):
        super().__init__()
        self.moji_server = moji_server
        self.busy_signal = busy_signal
        self.log_signal = log_signal

    def run(self) -> None:
        self.busy_signal.emit(True)
        self.log_signal.emit('')
        model = utils.prepare_model(mw.col)
        imported_count = 0
        skipped_count = 0
        for r in self.moji_server.fetch_all_from_server():
            note_dupes = mw.col.findNotes(f'target_id:"{r.target_id}"', f'deck:{utils.DECK_NAME}')
            if note_dupes:
                skipped_count += 1
                self.log_signal.emit(f'跳过重复单词:{r.target_id} {r.title}')
                continue
            storage.save_tts_file(r.target_id, self.moji_server.get_tts_url(r))
            note = notes.Note(mw.col, model)
            note['target_id'] = r.target_id
            note['target_type'] = str(r.target_type)
            note['sound'] = f'[sound:moji_{r.target_id}.mp3]'
            note['link'] = f'<a href="https://www.mojidict.com/details/{r.target_id}">Moji Web</a>'
            note['spell'] = r.spell
            note['pron'] = r.pron
            note['excerpt'] = r.excerpt
            note['accent'] = r.accent
            note['title'] = r.title
            mw.col.addNote(note)
            imported_count += 1
            self.log_signal.emit(f'增加单词:{r.target_id} {r.title}')
        self.log_signal.emit(f'执行结束,共增加{imported_count}个单词,跳过{skipped_count}个单词')
        self.busy_signal.emit(False)
