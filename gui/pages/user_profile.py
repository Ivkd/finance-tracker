from tkinter import filedialog
from gui.theme.dark import color
from gui.translate import t
import customtkinter as ctk
from PIL import Image

class UserProfilePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        main = ctk.CTkFrame(self, fg_color=color["BG"])
        main.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(main, fg_color=color["SIDEBAR"], corner_radius=18)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(header, text="User Profile", font=("Arial", 20, "bold")
                     ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

        body = ctk.CTkFrame(main, fg_color=color["CARD"], corner_radius=16)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(1, weight=1)

        # Аватар
        self.avatar_img = None
        self.avatar_lbl = ctk.CTkLabel(body, text="No Avatar", width=120, 
                                       height=120, corner_radius=8, fg_color="#0f1930")
        self.avatar_lbl.grid(row=0, column=0, rowspan=3, padx=16, pady=16)

        ctk.CTkButton(body, text="Upload", command=self.upload_avatar
                      ).grid(row=3, column=0, padx=16, pady=(0,16))

        # Поля
        ctk.CTkLabel(body, text="Name").grid(row=0, column=1, sticky="w", 
                                             padx=8, pady=(16, 4))
        self.name_entry = ctk.CTkEntry(body, placeholder_text="Your name", height=36)
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=4)

        ctk.CTkLabel(body, text="Email").grid(row=2, column=1, sticky="w", 
                                              padx=8, pady=(16, 4))
        self.email_entry = ctk.CTkEntry(body, placeholder_text="you@example.com", height=36)
        self.email_entry.grid(row=3, column=1, sticky="ew", padx=8, pady=4)

        ctk.CTkButton(body, text="Save", command=self.save_profile, fg_color=color["H_BUTTON"]
                      ).grid(row=4, column=1, sticky="e", padx=8, pady=16)

        # Хранилище профиля в памяти
        self.profile = {"name": "", "email": "", "avatar_path": None}

    def upload_avatar(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")])
        if not path:
            return
        self.profile["avatar_path"] = path
        img = Image.open(path).resize((120, 120))
        self.avatar_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
        self.avatar_lbl.configure(text="", image=self.avatar_img)

    def save_profile(self):
        self.profile["name"] = self.name_entry.get().strip()
        self.profile["email"] = self.email_entry.get().strip()

