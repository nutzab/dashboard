from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 100, 0, 0)
        layout.setSpacing(15)
        layout.addSpacing(50)
        self.Label1 = QLabel("Financial Manager")
        self.Label1.setObjectName("label1")

        self.btn_choice_group = QButtonGroup(self)

        self.btn1 = QPushButton("Dashboard")
        self.btn1.setMinimumHeight(80)
        self.btn1.setMinimumWidth(300)
        self.btn1.setCheckable(True)
        self.btn1.setChecked(True)

        self.btn2 = QPushButton("Analytics")
        self.btn2.setMinimumHeight(80)
        self.btn2.setMinimumWidth(300)
        self.btn2.setCheckable(True)

        self.btn3 = QPushButton("Calendar")
        self.btn3.setMinimumHeight(80)
        self.btn3.setMinimumWidth(300)
        self.btn3.setCheckable(True)

        self.btn4 = QPushButton("Transactions")
        self.btn4.setMinimumHeight(80)
        self.btn4.setMinimumWidth(300)
        self.btn4.setCheckable(True)

        self.btn5 = QPushButton("Budget")
        self.btn5.setMinimumHeight(80)
        self.btn5.setMinimumWidth(300)
        self.btn5.setCheckable(True)

        self.btn6 = QPushButton("Profile")
        self.btn6.setMinimumHeight(80)
        self.btn6.setMinimumWidth(300)
        self.btn6.setCheckable(True)

        self.btn7 = QPushButton("Settings")
        self.btn7.setMinimumHeight(80)
        self.btn7.setMinimumWidth(300)
        self.btn7.setCheckable(True)

        btn_list = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7]
        for i, btn in enumerate(btn_list):
            btn.setObjectName("btn")
            self.btn_choice_group.addButton(btn, i)

        layout.setSpacing(25)
        layout.addStretch()
        layout.addWidget(self.Label1, alignment=Qt.AlignCenter)
        layout.addSpacing(25)
        layout.addWidget(self.btn1, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn3, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn4, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn5, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn6, alignment=Qt.AlignHCenter)
        layout.addWidget(self.btn7, alignment=Qt.AlignHCenter)
        layout.addStretch(100)