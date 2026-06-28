import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from analytics import FinancialAnalytics


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("DashboardWindow")

        right_layout = QVBoxLayout(self)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        self.widget1 = QWidget()
        self.widget1.setObjectName("widget1")
        widget1_layout = QVBoxLayout(self.widget1)

        self.spend_label = QLabel("Spending mix")
        self.spend_label.setObjectName("s_label")
        widget1_layout.addWidget(self.spend_label)
        widget1_layout.addStretch()

        self.widget2 = QWidget()
        self.widget2.setObjectName("widget2")

        self.widget2_layout = QVBoxLayout(self.widget2)

        self.balance_label = QLabel("Monthly Income")
        self.balance_label.setObjectName("MI_label")
        self.widget2_layout.addWidget(self.balance_label)

        self.health_score_label = QLabel("Financial Health: Loading")
        self.health_score_label.setStyleSheet("font-size: 14px; color: #555555; margin-top: 10px;")
        self.widget2_layout.addWidget(self.health_score_label)

        self.top_expense_label = QLabel("Top expense category: Loading")
        self.top_expense_label.setStyleSheet("font-size: 14px; color: #555555; margin-top: 5px;")
        self.widget2_layout.addWidget(self.top_expense_label)

        self.widget2_layout.addStretch()

        top_row.addWidget(self.widget1, 1)
        top_row.addWidget(self.widget2, 1)

        right_layout.addLayout(top_row)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(20)

        self.widget3 = QWidget()
        self.widget3.setObjectName("widget3")
        self.widget3_layout = QVBoxLayout(self.widget3)
        self.bp_label = QLabel("Budget Progress")
        self.bp_label.setObjectName("bp_label")
        self.widget3_layout.addWidget(self.bp_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_layout.setSpacing(15)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.widget3_layout.addWidget(self.scroll_area)

        self.prediction_label = QLabel("Forecast: Calculating...")
        self.prediction_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #3f37c9; margin-top: 15px; padding: 10px; background-color: #f0f0f5; border-radius: 5px;")
        self.widget3_layout.addWidget(self.prediction_label)

        bottom_row.addWidget(self.widget3)
        right_layout.addLayout(bottom_row)
        right_layout.addStretch()

        self.load_analytics_data()

    def load_analytics_data(self):
        try:
            inc_exp = FinancialAnalytics.get_income_vs_expense_graph()
            self.spend_label.setText(f"Monthly Spendings: {inc_exp['expense']} GEL")
            self.balance_label.setText(f"Monthly Income: {inc_exp['income']} GEL")

            health_score = FinancialAnalytics.get_financial_health_score()
            self.health_score_label.setText(f"Financial Health Score:  {health_score} / 100")

            top_expenses = FinancialAnalytics.get_top_expenses()
            most_expensive_cat = top_expenses.get('most_expensive_category', ' None')
            max_cat_amount = top_expenses.get("max_cat_amount", 0.0)

            if most_expensive_cat != 'None' and max_cat_amount > 0:
                self.top_expense_label.setText(f"Highest Spending Category: {most_expensive_cat} ({max_cat_amount}) GEL")
            else:
                self.top_expense_label.setText("No expense data recorded yet.")

            prediction_text = FinancialAnalytics.predict_month_end_expense()
            self.prediction_label.setText(f'Forecast: {prediction_text}')

            for i in reversed(range(self.scroll_layout.count())):
                widget_to_remove = self.scroll_layout.itemAt(i).widget()
                if widget_to_remove is not None:
                    widget_to_remove.setParent(None)

            budgets = FinancialAnalytics.get_budget_status()
            if budgets:
                for b in budgets:
                    budget_widget = QWidget()
                    budget_item_layout = QVBoxLayout(budget_widget)

                    info_text = f"{b['category'].capitalize()} - Spent: {b['spent']} GEL / Limit: {b['limit']} GEL (Remaining: {b['remaining']} GEL)"
                    info_label = QLabel(info_text)
                    info_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #333;")

                    p_bar = QProgressBar()
                    p_bar.setRange(0, 100)
                    percentage = int(b['percentage'])
                    p_bar.setValue(min(percentage, 100))

                    if percentage >= 100:
                        p_bar.setStyleSheet("QProgressBar::chunk { background-color: #ef233c; }")
                    elif percentage >= 80:
                        p_bar.setStyleSheet("QProgressBar::chunk { background-color: #ffb703; }")
                    else:
                        p_bar.setStyleSheet("QProgressBar::chunk { background-color: #2a9d8f; }")

                    budget_item_layout.addWidget(info_label)
                    budget_item_layout.addWidget(p_bar)
                    self.scroll_layout.addWidget(budget_widget)
            else:
                no_budget_lbl = QLabel("No budget limits set yet. Go to settings/profile to add category limits.")
                no_budget_lbl.setStyleSheet("color: gray; font-style: italic; font-size: 14px;")
                self.scroll_layout.addWidget(no_budget_lbl)
        except Exception as e:
            print(f"Error loading analytics data into UI: {e}")