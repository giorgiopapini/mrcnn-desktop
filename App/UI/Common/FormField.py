from tkinter import *
import constants


class FormField(Entry):
    def __init__(self, root=None, input_type=constants.DataTypes.INT, initial_text='', **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.input_type = input_type.value

        self.initial_text = initial_text
        self.insert(0, self.initial_text)

        self.bind("<KeyRelease>", self.__get_input)

    def __get_input(self, event):
        if not event.keysym_num == constants.BACKSPACE_KEYSYM_NUM:
            self.validate_input()

    def validate_input(self):
        is_text_valid = self.input_type.is_valid(self.get())
        if not is_text_valid:
            self.delete(0, END)
            self.insert(0, self.initial_text)
