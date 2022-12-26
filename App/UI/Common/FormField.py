from tkinter import *
import constants
from App.UI.Common.SettingsDecoder import SettingsDecoder


class FormField(Entry):
    def __init__(self, root=None, input_type=constants.DataTypes.INT, setting='', **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.input_type = input_type.value

        self.setting = setting
        if self.setting is not '':
            self.initial_text = SettingsDecoder[self.setting]
        else:
            self.initial_text = ''
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

    def update_setting(self):
        converted_data = self.input_type.get_converted_data(self.get())
        SettingsDecoder.set_attribute(self.setting, converted_data)

    def override_text(self, text):
        self.clear_form()
        self.insert(0, text)

    def clear_form(self):
        self.delete(0, END)
