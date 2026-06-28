import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from sidebar import Sidebar
from dashboard import DashboardPage
from analytycsp import AnalyticsPage
from transactions import TransactionsPage
from calendarp import CalendarPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("main")
        self.setWindowTitle("Financial Manager")
        self.setMinimumSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.sidebar = Sidebar()
        self.stack = QStackedWidget()

        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.stack, 4)

        # Order must match sidebar button order: btn1, btn2, btn3, btn4, btn5, btn6, btn7
        self.stack.addWidget(DashboardPage())     # index 0 -> btn1 (Dashboard)
        self.stack.addWidget(AnalyticsPage())      # index 1 -> btn2 (Analytics)
        self.stack.addWidget(CalendarPage())      # index 2 -> btn3 (Calendar)
        self.stack.addWidget(TransactionsPage())  # index 3 -> btn4 (Transactions)
        # self.stack.addWidget(BudgetPage())        # index 4 -> btn5 (Budget)
        # self.stack.addWidget(ProfilePage())       # index 5 -> btn6 (Profile)
        # self.stack.addWidget(SettingsPage())      # index 6 -> btn7 (Settings)

        self.sidebar.btn_choice_group.buttonClicked[int].connect(self.stack.setCurrentIndex)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    app = QApplication(sys.argv)
    with open(os.path.join(BASE_DIR, "styles.qss"), "r", encoding="utf-8") as s:
        style = s.read()
        app.setStyleSheet(style)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())