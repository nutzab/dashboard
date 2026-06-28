import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtGui import QPixmap
from database import initialize_db
from models import UserManager, FinanceManager



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

class LogInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # initialize_db()
        self.setWindowTitle("Log In")
        self.setFixedSize(800, 600)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.left_panel = ImagePanel("fim.jpg")
        self.right_panel = QWidget()

        
        
        self.right_panel.setStyleSheet("background-color: #ffffff;")

        main_layout.addWidget(self.left_panel, 1) 
        main_layout.addWidget(self.right_panel, 1)  

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setSpacing(25)

        self.Label = QLabel("Log In")
        self.Label.setAlignment(Qt.AlignCenter)
        self.Label.setStyleSheet("color: #5a3eb1; font-size: 35px; font-weight: bold;")

        right_layout.addWidget(self.Label)

        self.LineEdit1 = QLineEdit()
        self.LineEdit2 = QLineEdit()

        self.LineEdit1.setPlaceholderText("Email")
        self.LineEdit2.setPlaceholderText("Password")

        self.LineEdit1.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.LineEdit1.setMaximumWidth(450)
        self.LineEdit2.setStyleSheet("padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.LineEdit2.setEchoMode(QLineEdit.Password)
        self.LineEdit2.setMaximumWidth(450)

        self.EmailErrorLabel = QLabel("")
        self.EmailErrorLabel.setStyleSheet("color: red; font-size: 12px;")
        self.PasswordErrorLabel = QLabel("")
        self.PasswordErrorLabel.setStyleSheet("color: red; font-size: 12px;")
        right_layout.addWidget(self.LineEdit1)
        right_layout.addWidget(self.EmailErrorLabel)
        right_layout.addWidget(self.LineEdit2)
        right_layout.addWidget(self.PasswordErrorLabel)

        
        self.LogInButton = QPushButton("Log In")
        self.LogInButton.setStyleSheet("QPushButton { background-color: #5a3eb1; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }"
            "QPushButton:hover { background-color: #4a2e9e; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }"
            "QPushButton:pressed { background-color: #3a1e8f; color: #ffffff; font-size: 16px; padding: 10px;\
            border: none; border-radius: 9px; }")
        
        
        right_layout.addWidget(self.LogInButton)

        self.Label2 = QLabel("Don't have an account?")
        self.Label2.setAlignment(Qt.AlignCenter)
        self.Label2.setStyleSheet("color: black; font-size: 14px;")
        right_layout.addWidget(self.Label2)

        self.SignUpButton = QPushButton("Sign Up")
        self.SignUpButton.setStyleSheet("QPushButton { background-color: Transparent; color: #5a3eb1; \
font-size: 16px; padding: 10px;}"
            "QPushButton:hover { background-color: Transparent; color:#4a2e9e; font-size: 16px; padding: 10px;}"
            "QPushButton:pressed { background-color: Transparent; color:#3a1e8f;  font-size: 16px; padding: 10px;}")
        right_layout.addWidget(self.SignUpButton)

        self.SignUpButton.clicked.connect(self.open_signup)
        self.LogInButton.clicked.connect(self.open_dashboard)
    def open_signup(self):
            global signup_window
            from lastsignup import SignUpWindow
            signup_window = SignUpWindow()
            signup_window.show()
            self.hide()
            
    def open_dashboard(self):
            global dashboard_window
            from dashboard import DashboardWindow
            dashboard_window = DashboardWindow()
            dashboard_window.show()
            self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = LogInWindow()
    window.show()
    sys.exit(app.exec_())