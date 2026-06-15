import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        layout.addSpacing(50)
        self.Label1 = QLabel("financial manager")
        self.Label1.setAlignment(Qt.AlignCenter)
        self.Label1.setObjectName("label1")
        layout.addWidget(self.Label1)
        self.Label1.setMaximumHeight(30)
        layout.addSpacing(50)  # Add spacing between label and buttons
        

        self.btn1 = QPushButton("Dashboard")
        self.btn1.setObjectName("pushButton1")
        self.btn1.setMinimumHeight(80)
        self.btn1.setMinimumWidth(300)
        layout.addWidget(self.btn1, alignment=Qt.AlignHCenter)  # Center the button horizontally
        

        self.btn2 = QPushButton("Analytics")
        self.btn2.setObjectName("pushButton2")
        self.btn2.setMinimumHeight(80)
        self.btn2.setMinimumWidth(300)
        layout.addWidget(self.btn2, alignment=Qt.AlignHCenter)  # Center the button horizontally

        self.btn3 = QPushButton("Calendar")
        self.btn3.setObjectName("pushButton3")
        self.btn3.setMinimumHeight(80)
        self.btn3.setMinimumWidth(300)
        layout.addWidget(self.btn3, alignment=Qt.AlignHCenter)  # Center the button horizontally

        self.btn4 = QPushButton("Transactions")
        self.btn4.setObjectName("pushButton4")
        self.btn4.setMinimumHeight(80)
        self.btn4.setMinimumWidth(300)
        layout.addWidget(self.btn4, alignment=Qt.AlignHCenter)  # Center the button horizontally

        self.btn5 =QPushButton("Budget")
        self.btn5.setObjectName("pushButton5")
        self.btn5.setMinimumHeight(80)
        self.btn5.setMinimumWidth(300)
        layout.addWidget(self.btn5, alignment=Qt.AlignHCenter)  # Center the button horizontally

        self.btn6 = QPushButton("Profile")
        self.btn6.setObjectName("pushButton6")
        self.btn6.setMinimumHeight(80)
        self.btn6.setMinimumWidth(300)
        layout.addWidget(self.btn6, alignment=Qt.AlignHCenter)  # Center the button horizontally

        self.btn7 = QPushButton("Settings")
        self.btn7.setObjectName("pushButton7")
        self.btn7.setMinimumHeight(80)
        self.btn7.setMinimumWidth(300)
        layout.addWidget(self.btn7, alignment=Qt.AlignHCenter)  # Center the button horizontally

        layout.addStretch()  # Add stretch to push buttons to the top

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        screen = QApplication.primaryScreen().availableGeometry()
        self.setMinimumSize(800, 600)
        self.setObjectName("DashboardWindow")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.left_panel = Sidebar()
        self.right_panel = QWidget()
        self.right_panel.setObjectName("right_panel")

        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.right_panel, 4)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        # Top row
        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        # First card
        self.widget1 = QWidget()
        self.widget1.setObjectName("widget1")

        widget1_layout = QVBoxLayout(self.widget1)

        self.networth_label = QLabel("Net Worth")
        self.networth_label.setObjectName("networth_label")

        widget1_layout.addWidget(self.networth_label)
        widget1_layout.addStretch()

        # Second card
        self.widget2 = QWidget()
        self.widget2.setObjectName("widget2")

        widget2_layout = QVBoxLayout(self.widget2)

        self.balance_label = QLabel("Balance")
        self.balance_label.setObjectName("balance_label")

        widget2_layout.addWidget(self.balance_label)
        widget2_layout.addStretch()

        # Add cards to horizontal row
        top_row.addWidget(self.widget1, 1)
        top_row.addWidget(self.widget2, 1)

        # Add row to right panel
        right_layout.addLayout(top_row)

        # Push everything to top
        right_layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.qss", "r") as s:
        style = s.read()
        app.setStyleSheet(style)
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())
