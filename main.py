import multiprocessing
from tkinter import *

from App.UI.Common.SettingsDecoder import SettingsDecoder
from App.UI.HomePage.homepage import HomePage


def main():
    SettingsDecoder.load_settings_from_json()
    root = Tk()
    root.title("Detector")
    root.geometry('800x480')
    root.resizable(False, False)
    HomePage(root)
    root.mainloop()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
