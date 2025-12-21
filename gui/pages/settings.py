from gui.theme.dark import color
import customtkinter as ctk
from gui.translate import  LANG, LAN_EN, LAN_RU, t

class SettingPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.main = ctk.CTkScrollableFrame(self, fg_color=color["BG"], corner_radius=0,
                                           orientation="vertical")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main.grid(row=0, column=0, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self.main, corner_radius=18, fg_color=color["SIDEBAR"])
        top.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        top.grid_columnconfigure(0, weight=1)

        self.title_lbl = ctk.CTkLabel(top, text=t("settings.title"), 
                                      font=("Arial", 22, "bold"))
        self.title_lbl.grid(row=0, column=0, padx=18, pady=14, sticky="w")

        self.body()

    def body(self):
        content = ctk.CTkFrame(self.main, corner_radius=18, fg_color=color["SIDEBAR"])
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure((0, 1), weight=1)

        # Линия: переключатель
        def make_line_seting_sw(row, name_key):
            line = ctk.CTkFrame(content, corner_radius=18, fg_color="transparent")
            line.grid(row=row, column=0, sticky="ew", padx=18, pady=10)
            line.grid_columnconfigure(0, weight=1)
            line.grid_columnconfigure(1, weight=0, minsize=220)
            lbl = ctk.CTkLabel(line, text=t(name_key), font=("Arial", 18, "italic"))
            lbl.grid(row=0, column=0, sticky="w")
            sw = ctk.CTkSwitch(
                line, text="", switch_width=46, switch_height=22,
                border_width=0, fg_color=color["SERTCH"], progress_color=color["H_BUTTON"],
                button_color=color["SWITCH"], button_hover_color=color["H_SWITCH"]
            )
            sw.grid(row=0, column=1, sticky="e")
            # Дополнительно можно подключить смену light/dark
            return lbl, sw

        # Линия: выпадающая табличка 
        def make_line_seting_om(row, name_key):
            line = ctk.CTkFrame(content, corner_radius=18, fg_color="transparent")
            line.grid(row=row, column=0, sticky="ew", padx=18, pady=10)
            line.grid_columnconfigure(0, weight=1)
            line.grid_columnconfigure(1, weight=0, minsize=220)

            lbl = ctk.CTkLabel(line, text=t(name_key), font=("Arial", 18, "italic"))
            lbl.grid(row=0, column=0, sticky="w")

            values = ["Русский", "English"]

            def set_lan(choice: str):
                # Маппинг на файлы
                if choice == "Русский":
                    path, code = LAN_RU, "ru"
                elif choice == "English":
                    path, code = LAN_EN, "en"
                else:
                    return
                LANG.load(path, lang_code=code)

                lbl.configure(text=t("settings.language"))
                self.title_lbl.configure(text=t("settings.title"))

                self.winfo_toplevel().refresh_text()  

            om = ctk.CTkOptionMenu(
                line, values=values,
                width=160, height=36,
                command=set_lan,
                corner_radius=12, fg_color=color["CARD"], text_color="white",
                button_color=color["SIDEBAR"], button_hover_color=color["H_BUTTON"],
                dropdown_fg_color=color["SIDEBAR"], dropdown_hover_color=color["H_BUTTON"],
                dropdown_text_color="white", dynamic_resizing=False, anchor="w"
            )
            om.grid(row=0, column=1, sticky="e")
            return lbl, om

        self.lbl_theme, self.sw_theme = make_line_seting_sw(row=0, name_key="settings.theme")
        self.lbl_lang, self.om_lang = make_line_seting_om(row=1, name_key="settings.language")

    def refresh_text(self):
        self.title_lbl.configure(text=t("settings.title"))
        self.lbl_theme.configure(text=t("settings.theme"))
        self.lbl_lang.configure(text=t("settings.language"))
