import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class sidebar(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        with open("styles.qss", "r") as s:
            style = s.read()
            self.setStyleSheet(style)
        

        layout = QVBoxLayout(self)  
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
    

        self.Label1 = QLabel("financial manager")
        self.Label1.setAlignment(Qt.AlignCenter)
        self.Label1.setStyleSheet("background-color: transparent; color: black; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.Label1)
        self.Label1.setMaximumHeight(30)

        self.PushButton1 = QtWidgets.QPushButton("Dashboard")
        self.PushButton1.setStyleSheet("QPushButton { background-color: #3f10cc; color: white;" \
        "font-size: 16px; padding: 10px; border: none; border-radius: 5px;}" )
        layout.addWidget(self.PushButton1)

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        screen = QApplication.primaryScreen().availableGeometry()
        self.setMinimumSize(800, 600)
        self.setStyleSheet("QMainWindow { background-color: #2B5C9C; }")
        

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.left_panel = sidebar()
        self.right_panel = QWidget()
        

        self.right_panel.setStyleSheet("background-color: #ffffff;" \
        "border-radius: 20px;")

        main_layout.addWidget(self.left_panel, 1) 
        main_layout.addWidget(self.right_panel, 4)  

        

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())