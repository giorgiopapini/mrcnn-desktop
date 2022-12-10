from tkinter import *

import constants
from App.UI.Common.FormField import FormField
from App.UI.Common.SettingsDecoder import SettingsDecoder
from App.UI.page import Page


class SettingsPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/Settings/background.png"
    INFO_BTN_IMG_PATH = "App/UI/Settings/info.png"
    EXTRA_SHORT_FIELD_PATH = "App/UI/Settings/extra_short.png"
    SHORT_FIELD_PATH = "App/UI/Settings/short.png"
    MEDIUM_FIELD_PATH = "App/UI/Settings/medium.png"
    LONG_FIELD_PATH = "App/UI/Settings/long.png"
    BACK_ARROW_IMG_PATH = "App/UI/Settings/back_arrow.png"
    SAVE_BTN_IMG_PATH = "App/UI/Settings/save.png"

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.info_btn_img = PhotoImage(file=self.INFO_BTN_IMG_PATH)
        self.extra_short_field_img = PhotoImage(file=self.EXTRA_SHORT_FIELD_PATH)
        self.short_field_img = PhotoImage(file=self.SHORT_FIELD_PATH)
        self.medium_field_img = PhotoImage(file=self.MEDIUM_FIELD_PATH)
        self.long_field_img = PhotoImage(file=self.LONG_FIELD_PATH)
        self.back_arrow_img = PhotoImage(file=self.BACK_ARROW_IMG_PATH)
        self.save_btn_img = PhotoImage(file=self.SAVE_BTN_IMG_PATH)

        self.canvas = Canvas(
            self.root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background = self.canvas.create_image(
            463.0, 179.0,
            image=self.background_img
        )

        self.save_btn = Button(
            image=self.save_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.__try_save_new_env_variables,
            relief="flat",
            cursor="hand2"
        )

        self.save_btn.place(
            x=351, y=51,
            width=90,
            height=39
        )

        self.calibration_info_btn = Button(
            image=self.info_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.calibration_info_btn.place(
            x=715, y=131,
            width=20,
            height=20
        )

        self.scan_info_btn = Button(
            image=self.info_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.scan_info_btn.place(
            x=715, y=304,
            width=20,
            height=20
        )

        self.camera_info_btn = Button(
            image=self.info_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.camera_info_btn.place(
            x=355, y=131,
            width=20,
            height=20
        )

        self.back_arrow_btn = Button(
            image=self.back_arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page
            ),
            relief="flat",
            cursor="hand2"
        )

        self.back_arrow_btn.place(
            x=33, y=48,
            width=38,
            height=38
        )

        self.manual_scan_info_btn = Button(
            image=self.info_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.manual_scan_info_btn.place(
            x=355, y=304,
            width=20,
            height=20
        )

        self.start_scan_char_field = self.canvas.create_image(
            297.0, 192.5,
            image=self.medium_field_img
        )

        self.start_scan_char_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.CHAR,
            setting='SCAN_CHAR',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.start_scan_char_field.place(
            x=262, y=184.4,
            width=70,
            height=19
        )

        self.stop_camera_char_field = self.canvas.create_image(
            331.0, 217.5,
            image=self.medium_field_img
        )

        self.stop_camera_char_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.CHAR,
            setting='QUIT_CHAR',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.stop_camera_char_field.place(
            x=296, y=209.4,
            width=70,
            height=19
        )

        self.camera_address_info = self.canvas.create_image(
            279.5, 242.5,
            image=self.long_field_img
        )

        self.camera_address_info = FormField(
            root=self.root,
            input_type=constants.DataTypes.STR,
            setting='ADDRESS',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.camera_address_info.place(
            x=206, y=234.4,
            width=147,
            height=19
        )

        self.scan_duration_field = self.canvas.create_image(
            596.5, 366.5,
            image=self.short_field_img
        )

        self.scan_duration_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='SCAN_TIME',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.scan_duration_field.place(
            x=571, y=358.4,
            width=51,
            height=19
        )

        self.show_segment_length_char_field = self.canvas.create_image(
            308.5, 366.5,
            image=self.short_field_img
        )

        self.show_segment_length_char_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.CHAR,
            setting='SHOW_CHAR',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.show_segment_length_char_field.place(
            x=283, y=358.4,
            width=51,
            height=19
        )

        self.erase_segment_char_field = self.canvas.create_image(
            308.5, 391.5,
            image=self.short_field_img
        )

        self.erase_segment_char_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.CHAR,
            setting='ERASE_CHAR',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.erase_segment_char_field.place(
            x=283, y=383.4,
            width=51,
            height=19
        )

        self.padding_field = self.canvas.create_image(
            526.5, 418.5,
            image=self.extra_short_field_img
        )

        self.padding_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='PADDING_PIXELS',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.padding_field.place(
            x=512, y=410.4,
            width=29,
            height=19
        )

        self.center_boundary_field = self.canvas.create_image(
            610.5, 391.5,
            image=self.short_field_img)

        self.center_boundary_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='CENTER_BOUNDARY_PIXELS',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.center_boundary_field.place(
            x=585, y=383.4,
            width=51,
            height=19
        )

        self.chessboard_cols_field = self.canvas.create_image(
            547.0, 192.5,
            image=self.medium_field_img
        )

        self.chessboard_cols_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='CHESSBOARD_COLS',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.chessboard_cols_field.place(
            x=512, y=184.4,
            width=70,
            height=19
        )

        self.chessboard_rows_field = self.canvas.create_image(
            680.0, 192.5,
            image=self.medium_field_img
        )

        self.chessboard_rows_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='CHESSBOARD_ROWS',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.chessboard_rows_field.place(
            x=645, y=184.4,
            width=70,
            height=19
        )

        self.calibration_images_needed_field = self.canvas.create_image(
            629.0, 217.5,
            image=self.medium_field_img
        )

        self.calibration_images_needed_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.INT,
            setting='CALIBRATION_IMAGES_NEEDED',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.calibration_images_needed_field.place(
            x=594, y=209.4,
            width=70,
            height=19
        )

        self.save_img_char_field = self.canvas.create_image(
            694.0, 242.5,
            image=self.medium_field_img
        )

        self.save_img_char_field = FormField(
            root=self.root,
            input_type=constants.DataTypes.CHAR,
            setting='SAVE_IMG_CHAR',
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify="center"
        )

        self.save_img_char_field.place(
            x=659, y=234.4,
            width=70,
            height=19
        )

    def __try_save_new_env_variables(self):
        self.start_scan_char_field.update_setting()
        self.stop_camera_char_field.update_setting()
        self.camera_address_info.update_setting()
        self.scan_duration_field.update_setting()
        self.show_segment_length_char_field.update_setting()
        self.erase_segment_char_field.update_setting()
        self.padding_field.update_setting()
        self.center_boundary_field.update_setting()
        self.chessboard_cols_field.update_setting()
        self.chessboard_rows_field.update_setting()
        self.calibration_images_needed_field.update_setting()
        self.save_img_char_field.update_setting()

        SettingsDecoder.save_current_settings_to_json()
        self.to_page(page=self.previous_page)

    def btn_clicked(self):
        pass
