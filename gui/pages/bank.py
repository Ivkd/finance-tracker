import customtkinter as ctk
from datetime import date
from gui.theme.dark import color
from gui.translate import t
import tkinter as tk
from tkinter import ttk, filedialog
from mem.Postgres import Start_PG


class BankPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.db = Start_PG()

        self.main = ctk.CTkFrame(self, fg_color=color["BG"])
        self.main.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        top = ctk.CTkFrame(self.main, corner_radius=18, fg_color=color["SIDEBAR"])
        top.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        top.grid_columnconfigure(1, weight=1)

        self.title_lbl = ctk.CTkLabel(top, text=t("bank.title"), font=("Arial", 22, "bold"))
        self.title_lbl.grid(row=0, column=0, padx=18, pady=14, sticky="w")

        # "Total: $0" -> через перевод (префикс "Total:")
        self.total_lbl = ctk.CTkLabel(
            top,
            text=f'{t("bank.total")}: $0',
            font=("Arial", 16, "bold"),
            text_color=color["H_BUTTON"]
        )
        self.total_lbl.grid(row=0, column=2, padx=18, pady=14, sticky="e")

        self.main_panel()

    def main_panel(self):
        actions = ctk.CTkFrame(self.main, fg_color="transparent")
        actions.grid(row=1, column=0, sticky="ew", pady=(0, 6))

        self.add_btn = ctk.CTkButton(actions, text=t("bank.actions.add"), command=self.add_tx)
        self.rm_btn  = ctk.CTkButton(actions, text=t("bank.actions.remove"), command=self.remove_selected, fg_color="#ef4444")
        self.exp_btn = ctk.CTkButton(actions, text=t("bank.actions.export_csv"), command=self.export_csv)

        self.add_btn.pack(side="left", padx=6)
        self.rm_btn.pack(side="left", padx=6)
        self.exp_btn.pack(side="left", padx=6)

        table_wrap = ctk.CTkFrame(self.main, corner_radius=16, fg_color=color["CARD"])
        table_wrap.grid(row=2, column=0, sticky="nsew")
        table_wrap.grid_rowconfigure(0, weight=1)
        table_wrap.grid_columnconfigure(0, weight=1)

        # Создание таблицы
        self.tree = ttk.Treeview(
            table_wrap,
            columns=("date", "desc", "amount", "category", "id"),
            show="headings",
            height=12
        )
        self.tree.heading("date", text=t("bank.table.date"))
        self.tree.heading("desc", text=t("bank.table.description"))
        self.tree.heading("amount", text=t("bank.table.amount"))
        self.tree.heading("category", text=t("bank.table.category"))
        self.tree.heading("id", text=t("bank.table.id"))

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("desc", width=300, anchor="w")
        self.tree.column("amount", width=50, anchor="e")
        self.tree.column("category", width=50, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        data = self.db.load_transaction()
        for row in data:
            id = row["id"]
            tx_type = row["type"]
            created_at = row["created_at"]
            category = row["category"]
            amount = float(row["amount"])
            self.tree.insert("", "end", values=(created_at, tx_type, f"{amount:.2f}", category, id))

        self.recalc_total()

    def recalc_total(self):
        self.summary = self.db.get_balance_summary()
        total = self.summary["balance"]
        self.total_lbl.configure(text=f'{t("bank.total")}: ${total:.2f}')

    def add_tx(self):
        win = tk.Toplevel(self.winfo_toplevel())
        win.title(t("bank.add_window.title"))
        win.resizable(False, False)
        win.grab_set()

        # Переменные
        tx_type_var = tk.StringVar(value="expense")
        category_var = tk.StringVar(value="")
        amount_var = tk.StringVar(value="0.00")

        # UI
        frm = ttk.Frame(win, padding=12)
        frm.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frm, text=t("bank.add_window.type")).grid(row=0, column=0, sticky="w", pady=(0, 6))
        type_cb = ttk.Combobox(
            frm, textvariable=tx_type_var,
            values=("income", "expense"),
            state="readonly", width=18
        )
        type_cb.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ttk.Label(frm, text=t("bank.add_window.category_name")).grid(row=1, column=0, sticky="w", pady=(0, 6))
        name_ent = ttk.Entry(frm, textvariable=category_var, width=22)
        name_ent.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ttk.Label(frm, text=t("bank.add_window.amount")).grid(row=2, column=0, sticky="w", pady=(0, 6))
        amount_ent = ttk.Entry(frm, textvariable=amount_var, width=22)
        amount_ent.grid(row=2, column=1, sticky="ew", pady=(0, 6))

        err_lbl = ttk.Label(frm, text="", foreground="red")
        err_lbl.grid(row=3, column=0, columnspan=2, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, sticky="e", pady=(10, 0))

        def submit():
            name = category_var.get().strip()
            if not name:
                err_lbl.config(text=t("bank.errors.enter_category"))
                return

            try:
                amount = float(amount_var.get().replace(",", "."))
            except ValueError:
                err_lbl.config(text=t("bank.errors.amount_number"))
                return

            tx_type = tx_type_var.get()
            date_now = str(date.today())

            row = self.db.add_transaction(created_at=date_now, tx_type=tx_type, category=name, amount=amount)
            tx_id = row["id"]

            # оставляю твою логику как есть (но обрати внимание: тут сейчас 4 значения, а колонок 5)
            self.tree.insert("", "end", values=(date_now, name, f"{amount:.2f}", tx_id))

            self.recalc_total()
            win.destroy()

        ttk.Button(btns, text=t("common.cancel"), command=win.destroy).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text=t("common.add"), command=submit).grid(row=0, column=1)

        name_ent.focus_set()
        win.bind("<Return>", lambda e: submit())
        win.bind("<Escape>", lambda e: win.destroy())

        frm.columnconfigure(1, weight=1)

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        for iid in selected:
            values = self.tree.item(iid)["values"]
            tx_id = int(values[-1])

            ok = self.db.remove_transaction(tx_id)
            self.tree.delete(iid)

        self.recalc_total()

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[(t("bank.export.filetype_csv"), "*.csv")]
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write("date,description,amount\n")
            for iid in self.tree.get_children():
                d, desc, amt = self.tree.item(iid)["values"]
                f.write(f"{d},{desc},{amt}\n")

    def refresh_text(self):
        # верх
        self.title_lbl.configure(text=t("bank.title"))  # [web:12][web:13]

        # total (оставляем сумму как есть)
        try:
            total = float(self.db.get_balance_summary()["balance"])
        except Exception:
            total = 0.0
        self.total_lbl.configure(text=f'{t("bank.total")}: ${total:.2f}')  # [web:12][web:13]

        # кнопки
        self.add_btn.configure(text=t("bank.actions.add"))  # [web:12][web:13]
        self.rm_btn.configure(text=t("bank.actions.remove"))  # [web:12][web:13]
        self.exp_btn.configure(text=t("bank.actions.export_csv"))  # [web:12][web:13]

        # заголовки таблицы (ttk.Treeview heading text)
        self.tree.heading("date", text=t("bank.table.date"))  # [web:38]
        self.tree.heading("desc", text=t("bank.table.description"))  # [web:38]
        self.tree.heading("amount", text=t("bank.table.amount"))  # [web:38]
        self.tree.heading("category", text=t("bank.table.category"))  # [web:38]
        self.tree.heading("id", text=t("bank.table.id"))  # [web:38]

