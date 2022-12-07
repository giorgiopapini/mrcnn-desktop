from tkinter import *


class Page(Frame):
    def __init__(self, root=None, **kwargs):
        Frame.__init__(self, root)
        self.root = root
        self.previous_page = kwargs.get("previous_page", None)
        self.homepage = kwargs.get("homepage", None)

    def to_page(self, page=None, **kwargs):
        if page is not None:
            page(self.root, **kwargs)

    @staticmethod
    def render_page(root=None, page=None, **kwargs):
        if page is not None:
            page(root, **kwargs)
