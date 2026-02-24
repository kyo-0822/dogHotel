import sys
import os
from database import db
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from signup import SignupWindow


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_path = os.path.join(base_dir, "UI", "login.ui")
from_class = uic.loadUiType(UI_path)[0]

class LoginWindow(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.db = db
        self.setupUi(self)
        self.login_ui()

    def login_ui(self):
        self.input_PW.setEchoMode(QLineEdit.Password)
        self.login_btn.clicked.connect(self.try_login)
        self.signup_btn.clicked.connect(self.signup_window_open)
    
    def try_login(self):
        input_email = self.input_ID.text().strip()
        input_pw = self.input_PW.text().strip()

        if not input_email or not input_pw :
            return
        
        is_success = self.db.login(input_email, input_pw)

        if is_success:
            self.main = DogHotel()
            self.main.show()
            self.close()
        else:
            self.input_PW.clear()
            self.input_PW.setFocus()
    
    def signup_window_open(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()


if __name__ == "__main__":
    import PyQt5
    import os
    qt_plugin_path = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5", "plugins", "platforms")
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
    
    app = QApplication(sys.argv)
    myWindow = LoginWindow()
    myWindow.show()
    sys.exit(app.exec_())