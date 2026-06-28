import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime
from models import FinanceManager


class TransactionsPage(QWidget):

    CATEGORIES = ["groceries", "transport", "entertainment", "health", "taxes", "salary", "other"]
    CURRENCIES = ["GEL", "USD", "EUR"]

    def __init__(self):
        super().__init__()
        self.setObjectName("right_panel")

        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        # ===== ტრანზაქციის დამატების ფორმა =====
        form_widget = QWidget()
        form_widget.setObjectName("form_card")
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(12)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(" Nikora, Wolt, aversi...")

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 1_000_000)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(10.00)

        self.currency_input = QComboBox()
        self.currency_input.addItems(self.CURRENCIES)

        self.type_input = QComboBox()
        self.type_input.addItems(["expense", "income"])

        self.category_input = QComboBox()
        self.category_input.addItems(self.CATEGORIES)

        self.date_input = QDateTimeEdit()
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.add_button = QPushButton("➕ add you transaction")
        self.add_button.clicked.connect(self.handle_add_transaction)

        self.form_error_label = QLabel("")
        self.form_error_label.setStyleSheet("color: red; font-size: 12px;")

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Currency:", self.currency_input)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("", self.add_button)
        form_layout.addRow("", self.form_error_label)

        right_layout.addWidget(form_widget)

        # ===== ტრანზაქციების ცხრილი =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Title", "Amount", "Currency", "Type", "Category", "Date", ""]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        right_layout.addWidget(self.table)

        self.load_transactions()

    # ---------- ლოგიკა ----------

    def handle_add_transaction(self):
        self.form_error_label.setText("")
        title = self.title_input.text().strip()

        if not title:
            self.form_error_label.setText("You must type in the title")
            return

        amount = self.amount_input.value()
        currency = self.currency_input.currentText()
        tx_type = self.type_input.currentText()
        date_str = self.date_input.dateTime().toString("yyyy-MM-dd HH:mm")

        try:
            FinanceManager.add_transaction(
                title=title,
                amount=amount,
                date=date_str,
                tx_type=tx_type,
                currency=currency,
            )
            self.title_input.clear()
            self.amount_input.setValue(10.00)
            self.load_transactions()
        except Exception as e:
            self.form_error_label.setText(f"Error: {e}")

    def load_transactions(self):
        try:
            df = FinanceManager.get_all_transactions_as_df()
        except Exception as e:
            print(f"Error loading transactions: {e}")
            return

        df = df.sort_values(by="date", ascending=False)
        self.table.setRowCount(0)

        for _, row in df.iterrows():
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)

            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row["title"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"{row['amount']:.2f}"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row["currency"])))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["type"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["category"])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row["date"])))

            delete_btn = QPushButton("🗑️")
            tx_id = row["id"]
            delete_btn.clicked.connect(lambda _, tid=tx_id: self.handle_delete(tid))
            self.table.setCellWidget(row_idx, 6, delete_btn)

    def handle_delete(self, tx_id):
        confirm = QMessageBox.question(
            self, "Delete", "Are you sure you really want to delete this transaction?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            FinanceManager.delete_transaction(tx_id)
            self.load_transactions()