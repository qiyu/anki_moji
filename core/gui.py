#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:qiyu.one@gmail.com
import json
import typing
from collections import deque

from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool, pyqtSignal, pyqtSlot, QRunnable
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QPlainTextEdit, QMessageBox, QCheckBox, QGroupBox

from . import utils, storage, common, anki
from .common import common_log
from .mojidict_server import MojiServer, MojiWord, MojiFolder


class LoginWindow(QDialog):
    def __init__(self, moji_server, parent=None):
        QDialog.__init__(self, parent)
        self.moji_server = moji_server

        self.login_field = QLineEdit()
        self.pass_field = QLineEdit()
        self.login_button = QPushButton("登录")

        self.init_window()
        self.show()

    def init_window(self):
        self.setWindowTitle('登录moji web')
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
        self.recursion_check_box = QCheckBox('同时导入一级子目录')
        self.update_check_box = QGroupBox('更新已有单词')
        self.update_spell_check_box = QCheckBox('更新拼写')
        self.update_accent_check_box = QCheckBox('更新声调')
        self.update_pron_check_box = QCheckBox('更新假名')
        self.update_exerpt_check_box = QCheckBox('更新摘要')
        self.update_sound_check_box = QCheckBox('更新发音')
        self.update_note_check_box = QCheckBox('更新笔记')
        self.update_pos_check_box = QCheckBox('更新词性')
        self.update_trans_check_box = QCheckBox('更新释义')
        self.update_examples_check_box = QCheckBox('更新例句')
        self.update_link_check_box = QCheckBox('更新链接')

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

        config = utils.get_config()
        self.model_name_field.setText(config.get('model_name') or 'Moji')
        self.deck_name_field.setText(config.get('deck_name') or 'Moji')
        self.dir_id_field.setText(config.get('dir_id') or '')
        self.recursion_check_box.setChecked(config.get('recursion') or False)
        self.update_check_box.setCheckable(True)
        # 更新已有单词不是常用功能，故默认不勾选，无需存于config
        self.update_check_box.setChecked(False)
        self.update_spell_check_box.setChecked(False)
        self.update_accent_check_box.setChecked(False)
        self.update_pron_check_box.setChecked(False)
        self.update_exerpt_check_box.setChecked(False)
        self.update_sound_check_box.setChecked(False)
        self.update_note_check_box.setChecked(False)
        self.update_pos_check_box.setChecked(False)
        self.update_trans_check_box.setChecked(False)
        self.update_examples_check_box.setChecked(False)
        self.update_link_check_box.setChecked(False)
        import_form = QFormLayout()
        import_form.addRow(model_name_label, self.model_name_field)
        import_form.addRow(deck_name_label, self.deck_name_field)
        import_form.addRow(dir_id_label, self.dir_id_field)
        grid = QGridLayout()
        grid.addWidget(self.update_spell_check_box, 0, 0)
        grid.addWidget(self.update_accent_check_box, 0, 1)
        grid.addWidget(self.update_pron_check_box, 0, 2)
        grid.addWidget(self.update_exerpt_check_box, 0, 3)
        grid.addWidget(self.update_sound_check_box, 0, 4)
        grid.addWidget(self.update_note_check_box, 1, 0)
        grid.addWidget(self.update_pos_check_box, 1, 1)
        grid.addWidget(self.update_trans_check_box, 1, 2)
        grid.addWidget(self.update_examples_check_box, 1, 3)
        grid.addWidget(self.update_link_check_box, 1, 4)
        self.update_check_box.setLayout(grid)

        main_layout = QVBoxLayout()
        main_layout.addLayout(import_form)
        main_layout.addWidget(self.recursion_check_box)
        main_layout.addWidget(self.update_check_box)
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
        update_existing = set()
        if self.update_check_box.isChecked():
            if self.update_spell_check_box.isChecked():
                update_existing.add('spell')
            if self.update_accent_check_box.isChecked():
                update_existing.add('accent')
            if self.update_pron_check_box.isChecked():
                update_existing.add('pron')
            if self.update_exerpt_check_box.isChecked():
                update_existing.add('excerpt')
            if self.update_sound_check_box.isChecked():
                update_existing.add('sound')
            if self.update_note_check_box.isChecked():
                update_existing.add('note')
            if self.update_pos_check_box.isChecked():
                update_existing.add('part_of_speech')
            if self.update_trans_check_box.isChecked():
                update_existing.add('trans')
            if self.update_examples_check_box.isChecked():
                update_existing.add('examples')
            if self.update_link_check_box.isChecked():
                update_existing.add('link')
        if "\\" in deck_name or '"' in deck_name:
            QMessageBox.critical(self, '', 'Deck名称中不能包含"和\\')
            return

        utils.update_config(
            {'model_name': model_name, 'deck_name': deck_name, 'dir_id': dir_id, 'recursion': recursion})

        if model_name and deck_name:
            if common.no_anki_mode:
                model = None
            else:
                from aqt import mw
                model = anki.prepare_model(model_name, deck_name, mw.col)
                # 处理历史版本的noteType字段数据
                if anki.update_model_fields(model, mw.col):
                    reply = QMessageBox.question(self, '', '插件将会在对应的笔记模板中增加字段，用来保存例句信息，是否继续？')
                    if reply == QMessageBox.StandardButton.Yes:
                        anki.update_model_fields(model, mw.col, force=True)
                    else:
                        return

                # 处理历史版本的模板数据
                if anki.update_template(model, mw.col):
                    reply = QMessageBox.question(self, '', '插件将会自动更新对应的卡片模板，是否继续？')
                    if reply == QMessageBox.StandardButton.Yes:
                        anki.update_template(model, mw.col, force=True)
                    else:
                        return

                    QMessageBox.question(self, '', '为了已有单词的复习体验，建议更新已有单词的翻译、例句、链接字段。' + \
                                            '是否更新目前选中的moji目录ID中的本地已有卡片？（之后仍可手动勾选更新）')
                    if reply == QMessageBox.StandardButton.Yes:
                        self.update_trans_check_box.setChecked(True)
                        self.update_examples_check_box.setChecked(True)
                        self.update_link_check_box.setChecked(True)
                        update_existing.add('trans')
                        update_existing.add('examples')
                        update_existing.add('link')

            self.word_loader = WordLoader(self.moji_server, self.busy_signal, self.log_signal, model,
                                          model_name, deck_name, dir_id, recursion, update_existing)
            self.thread_pool.start(self.word_loader)
        else:
            QMessageBox.critical(self, '', 'Deck名称和Note名称必填')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        common_log('关闭导入窗口')
        if self.word_loader:
            self.word_loader.interrupt()
        self.thread_pool.waitForDone()


class WordLoader(QRunnable):
    def __init__(self, moji_server: MojiServer, busy_signal, log_signal, model, model_name, deck_name, dir_id,
                 recursion, update_existing):
        super().__init__()
        self.moji_server = moji_server
        self.busy_signal = busy_signal
        self.log_signal = log_signal
        self.model = model
        self.model_name = model_name
        self.deck_name = deck_name
        self.dir_id = dir_id
        self.interrupted = False
        self.recursion = recursion
        self.update_existing = update_existing

    def run(self) -> None:
        self.busy_signal.emit(True)
        try:
            self.save_words()
        finally:
            self.busy_signal.emit(False)

    def interrupt(self):
        self.interrupted = True

    def save_words(self):
        model = self.model

        self.log_signal.emit('')

        total_imported_count = 0
        total_updated_count = 0
        total_skipped_count = 0

        moji_folders: typing.Deque[MojiFolder] = deque()
        current_folder = None
        dir_id = self.dir_id

        while True:
            if current_folder is None or current_folder.parent is None:
                if current_folder:
                    self.log_signal.emit('开始处理目录：' + current_folder.title)
                    dir_id = current_folder.target_id

                for r in self.moji_server.fetch_all_from_server(dir_id, current_folder):

                    if self.interrupted:
                        common_log('导入单词终止')
                        self.interrupted = False
                        return
                    elif isinstance(r, MojiWord):
                        duplicates = anki.check_duplicate(self.deck_name, r.target_id)
                        if duplicates:
                            if not self.update_existing:
                                self.log_signal.emit(f'跳过重复单词:{r.target_id} {r.title}')
                                total_skipped_count += 1
                            else:
                                for note in duplicates:
                                    self.update_note(note, r, self.update_existing)
                                self.log_signal.emit(f'更新已有单词:{r.target_id} {r.title}' 
                                                     + (f' (x{len(duplicates)})' if len(duplicates) > 1 else ''))
                                total_updated_count += len(duplicates)
                        else:
                            self.process_word(r, model)
                            self.log_signal.emit(f'增加单词:{r.target_id} {r.title}')
                            total_imported_count += 1
                    elif self.recursion:
                        moji_folders.append(r)

            if not moji_folders:
                break
            current_folder = moji_folders.popleft()

        self.log_signal.emit(f'执行结束,共增加{total_imported_count}个单词,更新{total_updated_count}个单词,跳过{total_skipped_count}个单词')

    def process_word(self, r: MojiWord, model):
        if common.no_anki_mode:
            common_log(f'获取到单词{r.title}')

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
                mw.col.addNote(note)
            except Exception:
                common_log('添加单词异常:' + json.dumps(r.__dict__, ensure_ascii=False))
                raise

    def update_note(self, note, word, update_keys):
        for key in update_keys:
            if key == 'note':
                # 'note' not implemented
                pass
            elif key == 'link':
                note[key] = utils.get_link(word)
            elif key == 'sound':
                note[key] = f'[sound:moji_{word.target_id}.mp3]'
                file_path = storage.get_file_path(word.target_id)
                content = self.moji_server.get_tts_url_and_download(word)
                storage.save_tts_file(file_path, content)
            else:
                note[key] = getattr(word, key)


def activate_import(moji_server):
    if not login_if_need(moji_server):
        return

    import_window = ImportWindow(moji_server)
    import_window.exec()


def activate_update(window, moji_server):
    if not login_if_need(moji_server):
        return

    try:
        note, target_id, target_type, title = anki.get_current_review_note()
    except Exception as e:
        QMessageBox.critical(window, '', str(e))
        return

    word = moji_server.fetch_single_word(target_id, target_type, title)

    # 更新发音文件
    tts_file_content = moji_server.get_tts_url_and_download(word)
    file_path = storage.get_file_path(target_id)
    storage.save_tts_file(file_path, tts_file_content)

    try:
        anki.refresh_current_note(note, word)
    except Exception as e:
        QMessageBox.critical(window, '', str(e))
        return

    QMessageBox.information(window, '', f'更新[{target_id} {title}]成功')


def login_if_need(moji_server) -> bool:
    if moji_server.session_valid():
        return True

    login_window = LoginWindow(moji_server)
    login_window.exec()

    return moji_server.session_valid()
