import numpy
import pandas
import matplotlib
import tkinter as tk

from gui.gui import MenuFinT


if __name__ == "__main__":
    root = tk.Tk()

    app = MenuFinT(root)

    root.mainloop()