import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from database import db

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_path = os.path.join(base_dir, "UI", "signup.ui")
from_class = uic.loadUiType(UI_path)[0]

class SignupWindow(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.input_password.setEchoMode(QLineEdit.Password)
        self.signup.clicked.connect(self.try_signup)

    def try_signup(self):
        name = self.input_name.text().strip()
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        if not name or not email or not password:
            return
        
        is_success = self.db.signup(name, email, password)

        if is_success:
            QMessageBox.information(self, "가입완료", "회원가입이 완료 됐습니다.")
            self.close()
        else:
            QMessageBox.critical(self, "가입 실패", "계정이 중복됩니다.")
            self.input_email.clear()
            self.input_password.clear()
            self.input_email.setFocus()