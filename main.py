import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class BudgetTracker:
    def __init__(self, filename="budget_data.json"):
        self.filename = filename
        self.transactions = []
        self.load_data()

    def add_transaction(self, amount, category, description):
        transaction = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
        self.save_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.transactions = json.load(f)

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.transactions, f, indent=4)

    def get_summary(self):
        summary = {}
        total_income = 0
        total_expense = 0
        for t in self.transactions:
            amount = t["amount"]
            category = t["category"]
            if category.lower() == "income":
                total_income += amount
            else:
                total_expense += amount
            summary[category] = summary.get(category, 0) + amount
        balance = total_income - total_expense
        return summary, total_income, total_expense, balance

    def list_transactions(self):
        return self.transactions

class BudgetApp:
    def __init__(self, root):
        self.tracker = BudgetTracker()
        self.root = root
        self.root.title("Budget Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.root, text="Amount")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(self.root, text="Category")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        self.description_label = tk.Label(self.root, text="Description")
        self.description_label.grid(row=2, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.summary_button = tk.Button(self.root, text="View Summary", command=self.show_summary)
        self.summary_button.grid(row=4, column=0, columnspan=2)

        self.tree = ttk.Treeview(self.root, columns=("Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.grid(row=5, column=0, columnspan=2)

        self.load_transactions()

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            self.tracker.add_transaction(amount, category, description)
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.load_transactions()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def show_summary(self):
        summary, income, expense, balance = self.tracker.get_summary()
        summary_msg = f"Total Income: ${income:.2f}\nTotal Expense: ${expense:.2f}\nBalance: ${balance:.2f}\n"
        for cat, amt in summary.items():
            summary_msg += f"{cat}: ${amt:.2f}\n"
        messagebox.showinfo("Summary", summary_msg)

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.tracker.list_transactions():
            self.tree.insert("", "end", values=(t["date"], t["category"], f"${t['amount']:.2f}", t["description"]))

def main():
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
