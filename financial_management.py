import json
import os

class FinancialManagement:
    def __init__(self):
        self.data_file = 'financial_data.json'
        self.deposits = []
        self.expenses = []
        self.fixed_expenses = []

        self.load_data()

    def add_deposit(self, amount):
        self.deposits.append(amount)
        self.save_data()

    def add_expense(self, description, amount, category):
        self.expenses.append((description, amount, category))
        self.save_data()

    def add_fixed_expense(self, description, amount, category):
        self.fixed_expenses.append((description, amount, category))
        self.save_data()

    def remove_deposit(self, index):
        del self.deposits[index]
        self.save_data()

    def remove_expense(self, index):
        del self.expenses[index]
        self.save_data()

    def remove_fixed_expense(self, index):
        del self.fixed_expenses[index]
        self.save_data()

    def calculate_balance(self):
        total_deposits = sum(self.deposits)
        total_expenses = sum(amount for _, amount, _ in self.expenses)
        total_fixed_expenses = sum(amount for _, amount, _ in self.fixed_expenses)
        return total_deposits - total_expenses - total_fixed_expenses

    def show_summary(self):
        summary = {
            "Depósitos": self.deposits,
            "Despesas": self.expenses,
            "Despesas Fixas": self.fixed_expenses,
            "Saldo": self.calculate_balance()
        }
        return summary

    def save_data(self):
        data = {
            "deposits": self.deposits,
            "expenses": self.expenses,
            "fixed_expenses": self.fixed_expenses
        }
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.deposits = data.get('deposits', [])
                self.expenses = data.get('expenses', [])
                self.fixed_expenses = data.get('fixed_expenses', [])
