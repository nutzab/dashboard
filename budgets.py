from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton
from models import FinanceManager


class BudgetPage(QWidget):

    # category_key -> display label (key must match what add_transaction() saves to the database)
    CATEGORY_DISPLAY = {
        "fun": "🎮 Fun",
        "groceries": "🥑 Groceries",
        "health": "🌿 Health",
        "rent": "🏠 Rent",
        "transport": "🚋 Transport",
        "savings": "💰 Savings",
    }

    def __init__(self):
        super().__init__()
        self.setObjectName("budget_panel")

        # this holds every category row, stacked top to bottom
        main_layout = QVBoxLayout(self)

        # we keep one spin box per category so Save knows which value to read
        self.spin_boxes = {}

        for category_key, display_label in self.CATEGORY_DISPLAY.items():
            row = self.create_category_row(category_key, display_label)
            main_layout.addWidget(row)

    def create_category_row(self, category_key, display_label):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)  # left-to-right layout for this one row

        # 1. the label
        label = QLabel(display_label)

        # 2. the number input
        spin_box = QDoubleSpinBox()
        spin_box.setPrefix("₾")
        spin_box.setRange(0, 1_000_000)
        self.spin_boxes[category_key] = spin_box  # remember it so Save can find it later

        # 3. the save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_category(category_key))

        row_layout.addWidget(label)
        row_layout.addWidget(spin_box)
        row_layout.addWidget(save_button)

        return row_widget

    def save_category(self, category_key):
        spin_box = self.spin_boxes[category_key]
        amount = spin_box.value()
        FinanceManager.set_budget(category_key, amount)
        print(f"Saved {category_key}: ₾{amount}")