import customtkinter as ctk
from gui.theme.dark import color
from gui.translate import t
import tkinter as tk

class ProjectPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.items = []

        wrap = ctk.CTkFrame(self, fg_color=color["BG"])
        wrap.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        wrap.grid_rowconfigure(2, weight=1)
        wrap.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(wrap, fg_color=color["SIDEBAR"], corner_radius=18)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ctk.CTkLabel(top, text=t("project.title"), font=("Arial", 20, "bold")
                     ).grid(row=0, column=0, padx=12, pady=10, sticky="w")

        entry_bar = ctk.CTkFrame(wrap, fg_color="transparent")
        entry_bar.grid(row=1, column=0, sticky="ew", pady=(0, 6))
        entry_bar.grid_columnconfigure(0, weight=1)
        self.task_entry = ctk.CTkEntry(entry_bar, placeholder_text="New task...", height=36)
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=6)
        ctk.CTkButton(entry_bar, text="Add", command=self.add_task
                      ).grid(row=0, column=1, padx=6)
        ctk.CTkButton(entry_bar, text="Remove checked", 
        command=self.remove_checked, fg_color="#ef4444").grid(row=0, column=2, padx=6)
        ctk.CTkButton(entry_bar, text="Complete all", command=self.complete_all, fg_color=color["H_BUTTON"]
                      ).grid(row=0, column=3, padx=6)

        self.list_frame = ctk.CTkScrollableFrame(wrap, corner_radius=16, fg_color=color["CARD"])
        self.list_frame.grid(row=2, column=0, sticky="nsew")

    def add_task(self):
        txt = self.task_entry.get().strip()
        if not txt:
            return
        var = tk.BooleanVar(value=False)
        row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        chk = ctk.CTkCheckBox(row, text=txt, variable=var)
        chk.pack(side="left", padx=6, pady=6)
        row.pack(fill="x", padx=6, pady=2)
        self.items.append((row, chk, var))
        self.task_entry.delete(0, "end")

    def remove_checked(self):
        keep = []
        for row, chk, var in self.items:
            if var.get():
                row.destroy()
            else:
                keep.append((row, chk, var))
        self.items = keep

    def complete_all(self):
        for _, chk, var in self.items:
            var.set(True)
