import json
import os
from datetime import datetime

DATA_FILE = 'budget_data.json'

class Transaction:
    def __init__(self, amount, category, trans_type, date=None):
        try:
            self.amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a number.")
        self.category = category
        self.trans_type = trans_type.lower()
        self.date = date if date else datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'trans_type': self.trans_type,
            'date': self.date
        }

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.transactions = [Transaction(**t) for t in data]
            except (json.JSONDecodeError, TypeError):
                print("Failed to load data. Starting with an empty transaction list.")
                self.transactions = []

    def save_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump([t.to_dict() for t in self.transactions], f, indent=4)
        except IOError:
            print("Failed to save data.")

    def add_transaction(self, amount, category, trans_type):
        try:
            t = Transaction(amount, category, trans_type)
            self.transactions.append(t)
            self.save_data()
        except ValueError as e:
            print(e)

    def view_summary(self):
        income = sum(t.amount for t in self.transactions if t.trans_type == 'income')
        expense = sum(t.amount for t in self.transactions if t.trans_type == 'expense')
        balance = income - expense
        print(f"\nSummary:")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expense: ${expense:.2f}")
        print(f"Current Balance: ${balance:.2f}")

    def view_by_category(self):
        category_totals = {}
        for t in self.transactions:
            if t.trans_type == 'expense':
                category_totals[t.category] = category_totals.get(t.category, 0) + t.amount
        print("\nExpenses by Category:")
        for cat, amt in category_totals.items():
            print(f"{cat}: ${amt:.2f}")

    def list_transactions(self):
        if not self.transactions:
            print("\nNo transactions recorded.")
            return
        print("\nAll Transactions:")
        for t in self.transactions:
            print(f"{t.date} | {t.trans_type.upper()} | ${t.amount:.2f} | {t.category}")

def main():
    tracker = BudgetTracker()
    while True:
        print("\n=== Budget Tracker ===")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View Expenses by Category")
        print("5. List All Transactions")
        print("6. Exit")
        choice = input("Select an option: ").strip()

        if choice == '1':
            amt = input("Enter income amount: ")
            cat = input("Enter income category: ").strip()
            tracker.add_transaction(amt, cat, 'income')
        elif choice == '2':
            amt = input("Enter expense amount: ")
            cat = input("Enter expense category: ").strip()
            tracker.add_transaction(amt, cat, 'expense')
        elif choice == '3':
            tracker.view_summary()
        elif choice == '4':
            tracker.view_by_category()
        elif choice == '5':
            tracker.list_transactions()
        elif choice == '6':
            print("Exiting Budget Tracker.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
