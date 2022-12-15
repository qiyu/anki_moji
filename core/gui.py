#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:qiyu.one@gmail.com
import json
import typing
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

import time
from time import strftime
from time import gmtime

from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QMessageBox, QCheckBox

from . import utils, storage, common
from .common import common_log
from .mojidict_server import MojiServer, MojiWord, MojiFolder


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
        self.pass_field.setEchoMode(QLineEdit.EchoMode.Password)
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
        self.recursion_check_box = QCheckBox()

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

        model_name_label = QLabel('笔记模板名称（Note）:')
        deck_name_label = QLabel('牌组名称（Deck）:')
        dir_id_label = QLabel('目录ID:')
        recursion_label = QLabel('同时导入1级子目录:')

        config = utils.get_config()
        self.model_name_field.setText(config.get('model_name') or 'Moji')
        self.deck_name_field.setText(config.get('deck_name') or 'Moji')
        self.dir_id_field.setText(config.get('dir_id') or '')
        self.recursion_check_box.setChecked(config.get('recursion') or False)
        import_form = QFormLayout()
        import_form.addRow(model_name_label, self.model_name_field)
        import_form.addRow(deck_name_label, self.deck_name_field)
        import_form.addRow(dir_id_label, self.dir_id_field)
        import_form.addRow(recursion_label, self.recursion_check_box)

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
        recursion = self.recursion_check_box.isChecked()
        if "\\" in deck_name or '"' in deck_name:
            QMessageBox.critical(self, '', 'Deck名称中不能包含"和\\')
            return

        utils.update_config(
            {'model_name': model_name, 'deck_name': deck_name, 'dir_id': dir_id, 'recursion': recursion})
        if model_name and deck_name:
            self.word_loader = WordLoader(self.moji_server, self.busy_signal, self.log_signal,
                                          model_name, deck_name, dir_id, recursion)
            self.thread_pool.start(self.word_loader)
        else:
            QMessageBox.critical(self, '', 'Deck名称和Note名称必填')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        common_log('关闭导入窗口')
        if self.word_loader:
            self.word_loader.interrupt()
        self.thread_pool.waitForDone()


class WordLoader(QRunnable):
    def __init__(self, moji_server, busy_signal, log_signal, model_name, deck_name, dir_id, recursion):
        super().__init__()
        self.moji_server = moji_server
        self.busy_signal = busy_signal
        self.log_signal = log_signal
        self.model_name = model_name
        self.deck_name = deck_name
        self.dir_id = dir_id
        self.interrupted = False
        self.recursion = recursion

    def run(self) -> None:
        self.busy_signal.emit(True)
        try:
            self.save_words()
        finally:
            self.busy_signal.emit(False)

    def interrupt(self):
        self.interrupted = True

    def save_words(self):
        start = time.time()
        if common.no_anki_mode:
            model = None
        else:
            from aqt import mw
            model = utils.prepare_model(self.model_name, self.deck_name, mw.col)

        self.log_signal.emit('')

        total_imported_count = 0
        total_skipped_count = 0
        total_fail_count = 0

        moji_folders: typing.Deque[MojiFolder] = deque()
        current_folder = None
        dir_id = self.dir_id

        while True:
            with ThreadPoolExecutor() as t:
                if current_folder is None or current_folder.parent is None:
                    if current_folder:
                        self.log_signal.emit('开始处理目录：' + current_folder.title)
                        dir_id = current_folder.target_id

                    res_list = []
                    for r in self.moji_server.fetch_all_from_server(dir_id, current_folder):
                        if self.interrupted:
                            common_log('导入单词终止')
                            self.interrupted = False
                            return

                        if isinstance(r, MojiWord):
                            res = t.submit(self.process_word, r, model)
                            res_list.append(res)
                        elif self.recursion:
                            moji_folders.append(r)

                    for future in as_completed(res_list):
                        if future.exception():
                            total_fail_count += 1
                        elif future.result():
                            total_imported_count += 1
                        else:
                            total_skipped_count += 1

            if not moji_folders:
                break
            current_folder = moji_folders.popleft()

        self.log_signal.emit(f'执行结束,用时: {strftime("%M:%S", gmtime(time.time() - start))}')
        self.log_signal.emit(f'共增加{total_imported_count}个单词,跳过{total_skipped_count}个单词,失败{total_fail_count}个单词')

    def process_word(self, r: MojiWord, model) -> bool:
        if common.no_anki_mode:
            common_log(f'获取到单词{r.title}')
        else:
            try:
                from aqt import mw
                note_dupes = mw.col.find_notes(f'deck:"{self.deck_name}" and target_id:{r.target_id}')
            except Exception:
                common_log('查询单词异常:' + json.dumps(r.__dict__, ensure_ascii=False))
                raise
            if note_dupes:
                self.log_signal.emit(f'跳过重复单词:{r.target_id} {r.title}')
                return False

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
            from anki import notes
            from aqt import mw
            note = notes.Note(mw.col, model)
            note['target_id'] = r.target_id
            note['target_type'] = str(r.target_type)
            note['sound'] = f'[sound:moji_{r.target_id}.mp3]'
            note['link'] = utils.get_link(r)
            note['spell'] = r.spell
            note['pron'] = r.pron
            note['excerpt'] = r.excerpt
            note['accent'] = r.accent
            note['title'] = r.title
            note['part_of_speech'] = r.part_of_speech
            note['trans'] = r.trans
            note['examples'] = r.examples
            try:
                from aqt import mw
                mw.col.addNote(note)
            except Exception:
                common_log('添加单词异常:' + json.dumps(r.__dict__, ensure_ascii=False))
                raise
        self.log_signal.emit(f'增加单词:{r.target_id} {r.title}')
        return True
