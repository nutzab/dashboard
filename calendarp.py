# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys



class CalendarPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("CalendarWindow")

        self.right_layout = QVBoxLayout(self)
        self.right_layout.setContentsMargins(20, 20, 20, 20)

        self.UiComponents()

        self.calendar.setLocale(
            QLocale(QLocale.English, QLocale.UnitedKingdom)
        )


        self.calendar.setFirstDayOfWeek(Qt.Monday)

    def UiComponents(self):
        self.calendar = QCalendarWidget()

        # Make it expand
        self.calendar.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.right_layout.addWidget(self.calendar)
        


