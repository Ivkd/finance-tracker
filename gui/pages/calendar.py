import customtkinter as ctk
from datetime import date
from gui.theme.dark import color
from gui.translate import t
import calendar

class CalendarPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.fg = ctk.CTkFrame(self, fg_color=color["BG"])
        self.fg.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notes = {}
        today = date.today()
        self.year = today.year
        self.month = today.month
        self.selected = today

        header = ctk.CTkFrame(self.fg, fg_color=color["SIDEBAR"], corner_radius=18)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(1, weight=1)
        self.title = ctk.CTkLabel(header, text=self._title_text(), 
                                  font=("Arial", 20, "bold"))
        self.title.grid(row=0, column=1, pady=10)

        prev_btn = ctk.CTkButton(header, text="◀", width=36, command=self.prev_month)
        next_btn = ctk.CTkButton(header, text="▶", width=36, command=self.next_month)
        prev_btn.grid(row=0, column=0, padx=10)
        next_btn.grid(row=0, column=2, padx=10)

        self.days = ctk.CTkFrame(self.fg, fg_color="transparent")
        self.days.grid(row=1, column=0, sticky="nsew")
        for i in range(7):
            self.days.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.days.grid_rowconfigure(i, weight=1)

        self.note_frame = ctk.CTkFrame(self.fg, fg_color=color["CARD"], corner_radius=16)
        self.note_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        self.note_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.note_frame, text="Note", font=("Arial", 14, "bold")
                     ).grid(row=0, column=0, sticky="w", padx=12, pady=(8, 2))
        self.note_entry = ctk.CTkEntry(self.note_frame, placeholder_text="Enter note...", 
                                       height=36)
        self.note_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=8)
        ctk.CTkButton(self.note_frame, text="Save", command=self.save_note
                      ).grid(row=1, column=1, padx=12)

        self.render_month()

    def _title_text(self):
        return f"{calendar.month_name[self.month]} {self.year}"

    def render_month(self):
        for w in self.days.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.days, text="Mo Tu We Th Fr Sa Su"
                     ).grid(row=0, column=0, columnspan=7, pady=6)
        mcal = calendar.Calendar(firstweekday=0)
        row = 1
        col = 0
        for day in mcal.itermonthdays(self.year, self.month):
            if day == 0:
                ctk.CTkLabel(self.days, text="").grid(row=row, column=col, padx=4, pady=4)
            else:
                d = date(self.year, self.month, day)
                btn = ctk.CTkButton(self.days, text=str(day), width=40, 
                                    command=lambda dd=d: self.select(dd))
                if d == self.selected:
                    btn.configure(fg_color=color["H_BUTTON"])
                btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            col += 1
            if col >= 7:
                col = 0
                row += 1

    def select(self, d: date):
        self.selected = d
        self.note_entry.delete(0, "end")
        self.note_entry.insert(0, self.notes.get(d.isoformat(), ""))  # показать заметку если есть
        self.render_month()

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.title.configure(text=self._title_text())
        self.render_month()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.title.configure(text=self._title_text())
        self.render_month()

    def save_note(self):
        self.notes[self.selected.isoformat()] = self.note_entry.get()
