import customtkinter as ctk

from gui.translate import t
from gui.theme.dark import color
from gui.pages.dashbord import DashboardPage
from gui.pages.bank import BankPage
from gui.pages.calendar import CalendarPage
from gui.pages.project import ProjectPage
from gui.pages.user_profile import UserProfilePage
from gui.pages.settings import SettingPage

from mem.Postgres import Start_PG

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  

#
## Приложение
#

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FTracker")
        self.geometry("1215x750")
        self.minsize(1215, 650)
        self.configure(fg_color=color["BG"])

        # Лэйаут
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure(1, weight=1)  

        self._build_sidebar()

        # Контент-область
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (DashboardPage, BankPage, 
                          CalendarPage, ProjectPage, 
                          UserProfilePage, SettingPage):
            page = PageClass(self.content)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")
        self.show_page("DashboardPage")

        self.db = Start_PG()

    def navigate(self, page_name: str):
        btn_map = {
            "DashboardPage": self.btn_dashboard,
            "BankPage": self.btn_bank,
            "CalendarPage": self.btn_calendar,
            "ProjectPage": self.btn_project,
            "UserProfilePage": self.btn_profile,
            "SettingPage": self.btn_settings,
        }
        btn = btn_map.get(page_name)
        if btn is not None:
            self.set_active(btn)
        self.show_page(page_name)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=18, fg_color=color["SIDEBAR"])
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.sidebar.grid_propagate(False)

        self.active_btn = None

        self.title_lbl = ctk.CTkLabel(
            self.sidebar, text=t("app.title"), font=("Arial", 18, "bold"))
        self.title_lbl.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        def build_button(text_key, page_name=None, row=None, exit_btn=False):
            btn = ctk.CTkButton(
                self.sidebar,
                text=t(text_key),
                anchor="w",
                height=40,
                corner_radius=12,
                fg_color="transparent",
                hover_color= color["H_BUTTON"] if not exit_btn else color["EXIT"],
                text_color="white",
                command=None
            )
            btn.grid(row=row, column=0, sticky="ew", padx=14, pady=6)
            if exit_btn:
                btn.configure(command=lambda: self.destroy())
            else:
                btn.configure(
                    btn.configure(command=lambda p=page_name: (self.navigate(p))))
            return btn

        self.btn_dashboard = build_button("nav.dashboard", "DashboardPage", row=1)
        self.btn_bank      = build_button("nav.bank", "BankPage", row=2)
        self.btn_calendar  = build_button("nav.calendar","CalendarPage", row=3)
        self.btn_project   = build_button("nav.project", "ProjectPage", row=4)
        self.btn_profile   = build_button("nav.profile", "UserProfilePage", row=5)
        self.btn_settings  = build_button("nav.settings", "SettingPage", row=6)
        self.btn_exit      = build_button("nav.exit", None, row=7, exit_btn=True)

        # Активируем первую
        self.set_active(self.btn_dashboard)
        self.sidebar.grid_columnconfigure(0, weight=1)

    def show_page(self, item):
        self.pages[item].tkraise()
        page = self.pages[item]
        if hasattr(page, "refresh_data"):
            page.refresh_data()

    def set_active(self, btn):
        if self.active_btn is not None:
            self.active_btn.configure(fg_color="transparent")
        btn.configure(fg_color=color["H_BUTTON"])
        self.active_btn = btn

    # Вызывается из SettingPage при смене языка, чтобы обновить тексты сайдбара
    def refresh_text(self):
        self.title_lbl.configure(text=t("app.title"))
        self.btn_dashboard.configure(text=t("nav.dashboard"))
        self.btn_bank.configure(text=t("nav.bank"))
        self.btn_calendar.configure(text=t("nav.calendar"))
        self.btn_project.configure(text=t("nav.project"))
        self.btn_profile.configure(text=t("nav.profile"))
        self.btn_settings.configure(text=t("nav.settings"))
        self.btn_exit.configure(text=t("nav.exit"))

        for page in self.pages.values():
            if hasattr(page, "refresh_text"):
                page.refresh_text()


if __name__ == "__main__":
    app = App()
    app.mainloop()
