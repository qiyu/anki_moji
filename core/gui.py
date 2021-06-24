#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Created by yu.qi on 2021/06/25.
# Mail:yu.qi@qunar.com
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QVBoxLayout


class MainWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle('从Moji导入')
        login_label = QLabel('用户:')
        pass_label = QLabel('密码:')
        self.login_field = QLineEdit()
        self.pass_field = QLineEdit()
        self.pass_field.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("登录")
        self.logout_button = QPushButton("注销")
        self.login_button.clicked.connect(self.login_button_clicked)
        self.logout_button.clicked.connect(self.logout_button_clicked)

        login_form = QFormLayout()
        login_form.addRow(login_label, self.login_field)
        login_form.addRow(pass_label, self.pass_field)

        main_layout = QVBoxLayout()

        self.setLayout(main_layout)
        self.show()

    def login_button_clicked(self):
        pass

    def logout_button_clicked(self):
        pass


if __name__ == '__main__':
    window = MainWindow()
    window.exec_()
