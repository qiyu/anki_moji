#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:qiyu.one@gmail.com
import json

from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QMessageBox

from aqt import mw

from . import utils, storage, common
from .common import common_log
from .mojidict_server import MojiServer, MojiWord


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
        try:
            self.moji_server.login(self.login_field.text(), self.pass_field.text())
        except Exception as e:
            QMessageBox.critical(self, '', '登录失败:' + str(e))
            return

        self.close()
        window = ImportWindow(self.moji_server)
        window.exec_()


class ImportWindow(QDialog):
    busy_signal = pyqtSignal(bool)
    log_signal = pyqtSignal(str)

    def __init__(self, moji_server, parent=None):
        QDialog.__init__(self, parent)
        self.moji_server: MojiServer = moji_server
        self.import_button = QPushButton('导入')
        self.model_name_field = QLineEdit()
        self.deck_name_field = QLineEdit()
        self.dir_id_field = QLineEdit()
        self.log_text = QPlainTextEdit()
        self.thread_pool = QThreadPool(self)
        self.thread_pool.setMaxThreadCount(1)
        self.word_loader = None
        self.busy_signal.connect(self.change_busy)
        self.log_signal.connect(self.add_log)
        self.init_window()
        self.show()

    def init_window(self):
        self.setWindowTitle('从Moji导入')
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumWidth(400)
        self.import_button.clicked.connect(self.import_button_clicked)
        model_name_label = QLabel('Note名称:')
        deck_name_label = QLabel('Deck名称:')
        dir_id_label = QLabel('目录ID:')
        config = utils.get_config()
        self.model_name_field.setText(config.get('model_name') or 'Moji')
        self.deck_name_field.setText(config.get('deck_name') or 'Moji')
        self.dir_id_field.setText('')
        import_form = QFormLayout()
        import_form.addRow(model_name_label, self.model_name_field)
        import_form.addRow(deck_name_label, self.deck_name_field)
        import_form.addRow(dir_id_label, self.dir_id_field)
        main_layout = QVBoxLayout()
        main_layout.addLayout(import_form)
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
        model_name = self.model_name_field.text().strip()
        deck_name = self.deck_name_field.text().strip()
        dir_id = self.dir_id_field.text().strip()
        utils.update_config({'model_name': model_name, 'deck_name': deck_name})
        if model_name and deck_name:
            self.word_loader = WordLoader(self.moji_server, self.busy_signal, self.log_signal,
                                          model_name, deck_name, dir_id)
            self.thread_pool.start(self.word_loader)
        else:
            QMessageBox.critical(self, '', 'Deck名称和Note名称必填')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        common_log('关闭导入窗口')
        if self.word_loader:
            self.word_loader.interrupt()
        self.thread_pool.waitForDone()


class WordLoader(QRunnable):
    def __init__(self, moji_server, busy_signal, log_signal, model_name, deck_name, dir_id):
        super().__init__()
        self.moji_server = moji_server
        self.busy_signal = busy_signal
        self.log_signal = log_signal
        self.model_name = model_name
        self.deck_name = deck_name
        self.dir_id = dir_id
        self.interrupted = False

    def run(self) -> None:
        self.busy_signal.emit(True)
        try:
            self.save_words()
        finally:
            self.busy_signal.emit(False)

    def interrupt(self):
        self.interrupted = True

    def save_words(self):
        if common.no_anki_mode:
            notes = None
            model = None
        else:
            from anki import notes
            model = utils.prepare_model(self.model_name, self.deck_name, mw.col)

        self.log_signal.emit('')

        imported_count = 0
        skipped_count = 0

        for r in self.moji_server.fetch_all_from_server(self.dir_id):
            if self.interrupted:
                common_log('导入单词终止')
                self.interrupted = False
                return

            if not isinstance(r, MojiWord):
                continue

            if common.no_anki_mode:
                common_log(f'获取到单词{r.title}')
            else:
                try:
                    note_dupes = mw.col.find_notes(f'deck:{self.deck_name} and target_id:{r.target_id}')
                except Exception:
                    common_log('查询单词异常:' + json.dumps(r.__dict__, ensure_ascii=False))
                    raise
                if note_dupes:
                    skipped_count += 1
                    self.log_signal.emit(f'跳过重复单词:{r.target_id} {r.title}')
                    continue

            file_path = storage.get_file_path(r.target_id)
            if not storage.has_file(file_path):
                try:
                    content = self.moji_server.get_tts_url_and_download(r)
                except Exception:
                    common_log(f'获取发音文件异常:{r.target_id} {r.title}')
                    self.log_signal.emit(f'获取发音文件异常:{r.target_id} {r.title}')
                    raise
                storage.save_tts_file(file_path, content)

            if common.no_anki_mode:
                common_log(f"虚拟保存note")
            else:
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
                try:
                    mw.col.addNote(note)
                except Exception:
                    common_log('添加单词异常:' + json.dumps(r.__dict__, ensure_ascii=False))
                    raise
            imported_count += 1
            self.log_signal.emit(f'增加单词:{r.target_id} {r.title}')
        self.log_signal.emit(f'执行结束,共增加{imported_count}个单词,跳过{skipped_count}个单词')
