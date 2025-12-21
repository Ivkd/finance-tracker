import customtkinter as ctk
from gui.theme.dark import color
from gui.translate import t
from mem.Postgres import Start_PG


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.main = ctk.CTkFrame(self, corner_radius=18, fg_color=color["BG"])
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main.grid(row=0, column=0, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self.main, corner_radius=18, fg_color=color["SIDEBAR"])
        top.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        top.grid_columnconfigure(1, weight=1)

        self.title_lbl = ctk.CTkLabel(top, text=t("dashboard.title"), font=("Arial", 22, "bold"))
        self.title_lbl.grid(row=0, column=0, padx=18, pady=14, sticky="w")

        self.search = ctk.CTkEntry(
            top,
            placeholder_text=t("dashboard.search_placeholder"),
            height=36,
            corner_radius=12,
            fg_color=color["SERTCH"],
            border_width=0
        )
        self.search.grid(row=0, column=1, padx=14, pady=14, sticky="ew")

        self.bell = ctk.CTkButton(
            top, text="🔔", width=44, height=36, corner_radius=12,
            fg_color=color["SERTCH"], hover_color=color["H_SERTCH"],
            command=lambda: self.go_to_page("CalendarPage")
        )
        self.bell.grid(row=0, column=2, padx=(0, 14), pady=14)

        self.make_body()

    def go_to_page(self, name_page):
        app = self.winfo_toplevel()
        app.navigate(name_page)
        
    def make_clickable(self, widget, callback):
        try:
            widget.configure(cursor="hand2")
        except Exception:
            pass
        widget.bind("<Button-1>", callback)

    def refresh_data(self):
        money = self.db.get_balance_summary()
        self.val_bal.configure(text=f"${float(money['balance']):.2f}")
        self.val_inc.configure(text=f"${float(money['total_income']):.2f}")
        self.val_spn.configure(text=f"${float(money['total_expense']):.2f}")


    def make_body(self):
        content = ctk.CTkFrame(self.main, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure((0, 1, 2, 3), weight=1)  # равные колонки [web:1]
        content.grid_rowconfigure((0, 1, 2), weight=1)

        def card(parent, title_key, value, r, c, colspan=1, rowspan=1):
            f = ctk.CTkFrame(parent, corner_radius=16, fg_color=color["CARD"])
            f.grid(row=r, column=c, columnspan=colspan, rowspan=rowspan,
                   sticky="nsew", padx=10, pady=10)
            lbl_title = ctk.CTkLabel(f, text=t(title_key), font=("Arial", 14, "bold"))
            lbl_title.pack(anchor="w", padx=14, pady=(12, 2))
            lbl_val = ctk.CTkLabel(f, text=value, font=("Arial", 20, "bold"), text_color=color["H_BUTTON"])
            lbl_val.pack(anchor="w", padx=14)
            return f, lbl_title, lbl_val

        self.db = Start_PG()
        self.money = self.db.get_balance_summary()

        # Сохраняем ссылки на подписи для refresh
        self.cards = []
        self.cards.append(card(content, "dashboard.balance", "—", 0, 0))
        self.cards.append(card(content, "dashboard.income", "—", 0, 1))
        self.cards.append(card(content, "dashboard.spending", "—", 0, 2))
        self.cards.append(card(content, "dashboard.savings", "$3711", 0, 3))

        self.val_bal = self.cards[0][2]
        self.val_inc = self.cards[1][2]
        self.val_spn = self.cards[2][2]
    
        (f_bal, lbl_bal, val_bal) = self.cards[0]
        (f_inc, lbl_inc, val_inc) = self.cards[1]
        (f_spn, lbl_spn, val_spn) = self.cards[2]
        (f_sav, lbl_sav, val_sav) = self.cards[3] 

        self.make_clickable(lbl_bal, lambda e: self.go_to_page("BankPage"))
        self.make_clickable(val_bal, lambda e: self.go_to_page("BankPage"))

        self.make_clickable(lbl_inc, lambda e: self.go_to_page("BankPage"))
        self.make_clickable(val_inc, lambda e: self.go_to_page("BankPage"))

        self.make_clickable(lbl_spn, lambda e: self.go_to_page("BankPage"))
        self.make_clickable(val_spn, lambda e: self.go_to_page("BankPage"))

        self.big = ctk.CTkFrame(content, corner_radius=16, fg_color=color["CARD"])
        self.big.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.big_lbl = ctk.CTkLabel(self.big, text=t("dashboard.revenue_placeholder"), 
                                    font=("Arial", 14, "bold"))
        self.big_lbl.pack(anchor="w", padx=14, pady=12)

        self.donut = ctk.CTkFrame(content, corner_radius=16, fg_color=color["CARD"])
        self.donut.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)
        self.donut_lbl = ctk.CTkLabel(self.donut, text=t("dashboard.total_earning_placeholder"), 
                                      font=("Arial", 14, "bold"))
        self.donut_lbl.pack(anchor="w", padx=14, pady=12)

        self.cov = ctk.CTkFrame(content, corner_radius=16, fg_color=color["CARD"])
        self.cov.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.cov_lbl = ctk.CTkLabel(self.cov, text=t("dashboard.coverage_placeholder"), 
                                    font=("Arial", 14, "bold"))
        self.cov_lbl.pack(anchor="w", padx=14, pady=12)

        self.met = ctk.CTkFrame(content, corner_radius=16, fg_color=color["CARD"])
        self.met.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.met_lbl = ctk.CTkLabel(self.met, text=t("dashboard.method_placeholder"), 
                                    font=("Arial", 14, "bold"))
        self.met_lbl.pack(anchor="w", padx=14, pady=12)

        self.tx = ctk.CTkFrame(content, corner_radius=16, fg_color=color["CARD"])
        self.tx.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)
        self.tx_lbl = ctk.CTkLabel(self.tx, text=t("dashboard.latest_transactions"), 
                                   font=("Arial", 14, "bold"))
        self.tx_lbl.pack(anchor="w", padx=14, pady=12)

        self.make_clickable(self.tx_lbl, lambda e: self.go_to_page("BankPage"))

    def refresh_text(self):
        self.title_lbl.configure(text=t("dashboard.title"))
        self.search.configure(placeholder_text=t("dashboard.search_placeholder"))
        # Карточки
        keys = ["dashboard.balance", "dashboard.income", 
                "dashboard.spending", "dashboard.savings"]
        for (frame, lbl_title, lbl_val), key in zip(self.cards, keys):
            lbl_title.configure(text=t(key))
        self.big_lbl.configure(text=t("dashboard.revenue_placeholder"))
        self.donut_lbl.configure(text=t("dashboard.total_earning_placeholder"))
        self.cov_lbl.configure(text=t("dashboard.coverage_placeholder"))
        self.met_lbl.configure(text=t("dashboard.method_placeholder"))
        self.tx_lbl.configure(text=t("dashboard.latest_transactions"))