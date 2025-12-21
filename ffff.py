import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-page app")
        self.geometry("900x600")

        # 1. Контейнер для всех страниц
        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        # чтобы все страницы растягивались
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 2. Создаём страницы и кладём в dict
        self.pages = {}
        for PageClass in (DashboardPage, BankPage, SettingsPage):
            page = PageClass(self.container, self)
            name = PageClass.__name__
            self.pages[name] = page
            page.grid(row=0, column=0, sticky="nsew")  # все в одну ячейку [web:294][web:303]

        # 3. Показать стартовую страницу
        self.show_page("DashboardPage")

        # 4. Простое боковое меню
        sidebar = ctk.CTkFrame(self, width=160, corner_radius=0)
        sidebar.place(x=0, y=0, relheight=1)

        ctk.CTkButton(sidebar, text="Dashboard",
                      command=lambda: self.show_page("DashboardPage")).pack(padx=10, pady=10, fill="x")
        ctk.CTkButton(sidebar, text="Bank",
                      command=lambda: self.show_page("BankPage")).pack(padx=10, pady=10, fill="x")
        ctk.CTkButton(sidebar, text="Settings",
                      command=lambda: self.show_page("SettingsPage")).pack(padx=10, pady=10, fill="x")

    def show_page(self, name: str):
        """Поднять нужный экран."""
        page = self.pages[name]
        page.tkraise()   # ключевая строчка: показывает выбранный фрейм [web:294][web:309]


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ctk.CTkLabel(self, text="DASHBOARD", font=("Arial", 24, "bold")).pack(pady=40)


class BankPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ctk.CTkLabel(self, text="BANK", font=("Arial", 24, "bold")).pack(pady=40)


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ctk.CTkLabel(self, text="SETTINGS", font=("Arial", 24, "bold")).pack(pady=40)


if __name__ == "__main__":
    app = App()
    app.mainloop()
