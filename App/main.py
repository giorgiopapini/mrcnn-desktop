from tkinter import *

from App.UI.Common.SettingsDecoder import SettingsDecoder
from App.UI.HomePage.homepage import HomePage
from App.UI.Recap.recap_page import RecapPage


def main():
    SettingsDecoder.load_settings_from_json()
    root = Tk()
    root.title("Detector")
    root.geometry('800x480')
    root.resizable(False, False)
    HomePage(root)
    #RecapPage(root)
    root.mainloop()


if __name__ == '__main__':
    main()
