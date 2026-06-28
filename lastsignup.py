import re
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtGui import QPixmap
from database import initialize_db
from models import UserManager, FinanceManager


signin_window = None

class ImagePanel(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        # center crop
        x = (scaled.width() - self.width()) // 2
        y = (scaled.height() - self.height()) // 2
        painter.drawPixmap(0, 0, scaled, x, y, self.width(), self.height())

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sign Up")
        self.setFixedSize(800, 600)

        
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.left_panel = ImagePanel("fim.jpg")
        self.right_panel = QWidget()

        
        
        self.right_panel.setStyleSheet("background-color: #ffffff;")

        main_layout.addWidget(self.left_panel, 1) 
        main_layout.addWidget(self.right_panel, 1)  

        right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setSpacing(25)

        

        self.Label = QLabel("Sign Up")
        self.Label.setAlignment(Qt.AlignCenter)
        self.Label.setStyleSheet("color: #5a3eb1; font-size: 35px; font-weight: bold;")

        right_layout.addWidget(self.Label)

        self.LineEdit1 = QtWidgets.QLineEdit()
        self.LineEdit2 = QtWidgets.QLineEdit()
        self.LineEdit3 = QtWidgets.QLineEdit()

        self.LineEdit3.setPlaceholderText("Username")
        self.LineEdit1.setPlaceholderText("Email")
        self.LineEdit2.setPlaceholderText("Password")

        self.LineEdit1.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.LineEdit1.setMaximumWidth(450)
        self.LineEdit2.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.LineEdit2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LineEdit2.setMaximumWidth(450)
        self.LineEdit3.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.LineEdit3.setMaximumWidth(450)

        self.EmailErrorLabel = QLabel("")
        self.EmailErrorLabel.setStyleSheet("color: red; font-size: 12px;")
        self.PasswordErrorLabel = QLabel("")
        self.PasswordErrorLabel.setStyleSheet("color: red; font-size: 12px;")
        self.UsernameErrorLabel = QLabel("")
        self.UsernameErrorLabel.setStyleSheet("color: red; font-size: 12px;")
        
        right_layout.addWidget(self.LineEdit3)
        right_layout.addWidget(self.UsernameErrorLabel)
        right_layout.addWidget(self.LineEdit1)
        right_layout.addWidget(self.EmailErrorLabel)
        right_layout.addWidget(self.LineEdit2)
        right_layout.addWidget(self.PasswordErrorLabel)

        self.LineEdit3.textChanged.connect(lambda: self.UsernameErrorLabel.setText(""))
        self.LineEdit1.textChanged.connect(lambda: self.EmailErrorLabel.setText(""))
        self.LineEdit2.textChanged.connect(lambda: self.PasswordErrorLabel.setText(""))
        
       
        
        self.SignUpButton = QtWidgets.QPushButton("Sign Up")
        self.SignUpButton.setStyleSheet("QPushButton { background-color: #5a3eb1; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }"
            "QPushButton:hover { background-color: #4a2e9e; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }"
            "QPushButton:pressed { background-color: #3a1e8f; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }")
        
        
        right_layout.addWidget(self.SignUpButton)

        self.Label2 = QLabel("Already have an account?")
        self.Label2.setAlignment(Qt.AlignCenter)
        self.Label2.setStyleSheet("color: black; font-size: 14px;")
        right_layout.addWidget(self.Label2)

        self.LogInButton = QtWidgets.QPushButton("Log In")
        self.LogInButton.setStyleSheet("QPushButton { background-color: Transparent; color: #5a3eb1; \
font-size: 16px; padding: 10px;}"
            "QPushButton:hover { background-color: Transparent; color:#4a2e9e; font-size: 16px; padding: 10px;}"
            "QPushButton:pressed { background-color: Transparent; color:#3a1e8f;  font-size: 16px; padding: 10px;}")
        right_layout.addWidget(self.LogInButton)

        self.LogInButton.clicked.connect(self.open_signin)
        self.SignUpButton.clicked.connect(self.handle_signup)


    def handle_signup(self):
        username = self.LineEdit3.text().strip()
        email = self.LineEdit1.text().strip()
        password = self.LineEdit2.text().strip()

        self.UsernameErrorLabel.setText("")
        self.EmailErrorLabel.setText("")
        self.PasswordErrorLabel.setText("")

        has_error = False

        if not username:
            self.UsernameErrorLabel.setText("Username is required")
            has_error = True

        if not email:
            self.EmailErrorLabel.setText("Email is required")
            has_error = True
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.EmailErrorLabel.setText("Enter a valid email (e.g. name@example.com)")
            has_error = True

        if not password:
            self.PasswordErrorLabel.setText("Password is required")
            has_error = True
        elif len(password) < 8:
            self.PasswordErrorLabel.setText("Password must be at least 8 characters")
            has_error = True

        if has_error:
            return

        success = UserManager.register_user(username, password)
        if success:
            self.open_signin() 
        else:
            self.UsernameErrorLabel.setText("Username already exists")

    def open_signin(self):
            global signin_window
            from lastsignin import LogInWindow
            signin_window = LogInWindow()
            signin_window.show()
            self.hide()
            
    
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    initialize_db()
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec_())