from tkinter import *

from App.UI.HomePage.homepage import HomePage
from decouple import config

from App.UI.Settings.settings_page import SettingsPage


def new_main():
    path = config("RESULTS_PATH")
    print(path)
    root = Tk()
    root.title("Detector")
    root.geometry('800x480')
    root.resizable(False, False)
    HomePage(root)
    root.mainloop()
