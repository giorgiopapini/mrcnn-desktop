from tkinter import *

from App.HomePage.homepage import HomePage


def new_main():
    root = Tk()
    root.title("Detector")
    root.geometry('800x480')
    root.resizable(False, False)
    HomePage(root)
    root.mainloop()
