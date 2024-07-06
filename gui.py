import tkinter as tk
from tkinter import messagebox
from financial_management import FinancialManagement

class FinancialApp:
    def __init__(self, root):
        self.fm = FinancialManagement()
        self.root = root
        self.root.title("Gestão Financeira")

        self.create_widgets()

    def create_widgets(self):
        # Labels and entries for Deposits
        self.deposit_label = tk.Label(self.root, text="Depósito")
        self.deposit_label.grid(row=0, column=0)
        self.deposit_entry = tk.Entry(self.root)
        self.deposit_entry.grid(row=0, column=1)
        self.deposit_button = tk.Button(self.root, text="Adicionar", command=self.add_deposit)
        self.deposit_button.grid(row=0, column=2)

        # Labels and entries for Expenses
        self.expense_label = tk.Label(self.root, text="Despesa")
        self.expense_label.grid(row=1, column=0)
        self.expense_entry = tk.Entry(self.root)
        self.expense_entry.grid(row=1, column=1)
        self.expense_amount_label = tk.Label(self.root, text="Valor")
        self.expense_amount_label.grid(row=2, column=0)
        self.expense_amount_entry = tk.Entry(self.root)
        self.expense_amount_entry.grid(row=2, column=1)
        self.expense_category_label = tk.Label(self.root, text="Categoria")
        self.expense_category_label.grid(row=3, column=0)
        self.expense_category_entry = tk.Entry(self.root)
        self.expense_category_entry.grid(row=3, column=1)
        self.expense_button = tk.Button(self.root, text="Adicionar", command=self.add_expense)
        self.expense_button.grid(row=4, column=1)

        # Labels and entries for Fixed Expenses
        self.fixed_expense_label = tk.Label(self.root, text="Despesa Fixa")
        self.fixed_expense_label.grid(row=5, column=0)
        self.fixed_expense_entry = tk.Entry(self.root)
        self.fixed_expense_entry.grid(row=5, column=1)
        self.fixed_expense_amount_label = tk.Label(self.root, text="Valor")
        self.fixed_expense_amount_label.grid(row=6, column=0)
        self.fixed_expense_amount_entry = tk.Entry(self.root)
        self.fixed_expense_amount_entry.grid(row=6, column=1)
        self.fixed_expense_category_label = tk.Label(self.root, text="Categoria")
        self.fixed_expense_category_label.grid(row=7, column=0)
        self.fixed_expense_category_entry = tk.Entry(self.root)
        self.fixed_expense_category_entry.grid(row=7, column=1)
        self.fixed_expense_button = tk.Button(self.root, text="Adicionar", command=self.add_fixed_expense)
        self.fixed_expense_button.grid(row=8, column=1)

        # Show summary
        self.summary_button = tk.Button(self.root, text="Mostrar Resumo", command=self.show_summary)
        self.summary_button.grid(row=9, column=1)

        # Summary display area with scrollbar
        self.summary_frame = tk.Frame(self.root)
        self.summary_frame.grid(row=10, column=0, columnspan=3, sticky='nsew')

        self.canvas = tk.Canvas(self.summary_frame)
        self.scrollbar = tk.Scrollbar(self.summary_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def add_deposit(self):
        amount = self.deposit_entry.get()
        if amount:
            self.fm.add_deposit(float(amount))
            self.deposit_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Depósito adicionado com sucesso!")
            self.show_summary()
        else:
            messagebox.showerror("Erro", "Valor do depósito não pode ser vazio")

    def add_expense(self):
        description = self.expense_entry.get()
        amount = self.expense_amount_entry.get()
        category = self.expense_category_entry.get()
        if description and amount and category:
            self.fm.add_expense(description, float(amount), category)
            self.expense_entry.delete(0, tk.END)
            self.expense_amount_entry.delete(0, tk.END)
            self.expense_category_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Despesa adicionada com sucesso!")
            self.show_summary()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def add_fixed_expense(self):
        description = self.fixed_expense_entry.get()
        amount = self.fixed_expense_amount_entry.get()
        category = self.fixed_expense_category_entry.get()
        if description and amount and category:
            self.fm.add_fixed_expense(description, float(amount), category)
            self.fixed_expense_entry.delete(0, tk.END)
            self.fixed_expense_amount_entry.delete(0, tk.END)
            self.fixed_expense_category_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Despesa fixa adicionada com sucesso!")
            self.show_summary()
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos")

    def remove_deposit(self, index):
        self.fm.remove_deposit(index)
        messagebox.showinfo("Sucesso", "Depósito removido com sucesso!")
        self.show_summary()

    def remove_expense(self, index):
        self.fm.remove_expense(index)
        messagebox.showinfo("Sucesso", "Despesa removida com sucesso!")
        self.show_summary()

    def remove_fixed_expense(self, index):
        self.fm.remove_fixed_expense(index)
        messagebox.showinfo("Sucesso", "Despesa fixa removida com sucesso!")
        self.show_summary()

    def show_summary(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        summary = self.fm.show_summary()

        tk.Label(self.scrollable_frame, text="Depósitos:").grid(row=0, column=0, sticky=tk.W)
        for i, deposit in enumerate(summary["Depósitos"]):
            tk.Label(self.scrollable_frame, text=str(deposit)).grid(row=i+1, column=0, sticky=tk.W)
            tk.Button(self.scrollable_frame, text="Remover", command=lambda i=i: self.remove_deposit(i)).grid(row=i+1, column=1)

        tk.Label(self.scrollable_frame, text="Despesas:").grid(row=len(summary["Depósitos"]) + 1, column=0, sticky=tk.W)
        for i, (desc, amt, cat) in enumerate(summary["Despesas"]):
            tk.Label(self.scrollable_frame, text=f"{desc}: {amt} ({cat})").grid(row=len(summary["Depósitos"]) + i + 2, column=0, sticky=tk.W)
            tk.Button(self.scrollable_frame, text="Remover", command=lambda i=i: self.remove_expense(i)).grid(row=len(summary["Depósitos"]) + i + 2, column=1)

        tk.Label(self.scrollable_frame, text="Despesas Fixas:").grid(row=len(summary["Depósitos"]) + len(summary["Despesas"]) + 2, column=0, sticky=tk.W)
        for i, (desc, amt, cat) in enumerate(summary["Despesas Fixas"]):
            tk.Label(self.scrollable_frame, text=f"{desc}: {amt} ({cat})").grid(row=len(summary["Depósitos"]) + len(summary["Despesas"]) + i + 3, column=0, sticky=tk.W)
            tk.Button(self.scrollable_frame, text="Remover", command=lambda i=i: self.remove_fixed_expense(i)).grid(row=len(summary["Depósitos"]) + len(summary["Despesas"]) + i + 3, column=1)

        tk.Label(self.scrollable_frame, text=f"Saldo: {summary['Saldo']}").grid(row=len(summary["Depósitos"]) + len(summary["Despesas"]) + len(summary["Despesas Fixas"]) + 3, column=0, sticky=tk.W)
