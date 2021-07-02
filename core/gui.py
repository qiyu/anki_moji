#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:yu.qi@qunar.com

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit
from aqt import mw

from . import utils
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
    def __init__(self, moji_server, parent=None):
        QDialog.__init__(self, parent)
        self.moji_server: MojiServer = moji_server

        self.import_button = QPushButton('导入')
        self.log_text = QPlainTextEdit()
        self.init_window()
        self.show()

    def init_window(self):
        self.setWindowTitle('从Moji导入')
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumWidth(300)
        self.import_button.clicked.connect(self.import_button_clicked)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.import_button)
        main_layout.addWidget(self.log_text)
        self.setLayout(main_layout)

    def import_button_clicked(self):
        # for r in self.server.fetch_all_from_server():
        #     storage.save_tts_file(r.target_id, self.moji_server.get_tts_url(r))
        utils.prepare_model(mw.col)

    def format_row(self, r):
        try:
            return '\t'.join([r.target_id, str(r.target_type),
                              r.title, r.spell, r.accent, r.pron, r.excerpt,
                              f'[sound:moji_{r.target_id}.mp3]',
                              f'<a href="https://www.mojidict.com/details/{r.target_id}">Moji Web</a>'])
        except Exception:
            print("处理异常", r.spell)
            raise
