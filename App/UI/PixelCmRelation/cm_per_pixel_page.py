import json
from tkinter import *
from App.ArucoDetection.aruco_detection import ArucoDetector
from App.UI.Common.FormField import FormField
from App.UI.page import Page
import constants


class CmPerPixelPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/PixelCmRelation/background.png"
    SCAN_BTN_IMG_PATH = "App/UI/ScanSelection/scan_btn.png"
    BACK_ARROW_IMG_PATH = "App/UI/Settings/back_arrow.png"
    FORM_FIELD_IMG_PATH = "App/UI/PixelCmRelation/form_field_img.png"

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.scan_btn_img = PhotoImage(file=self.SCAN_BTN_IMG_PATH)
        self.back_arrow_img = PhotoImage(file=self.BACK_ARROW_IMG_PATH)
        self.form_field_img = PhotoImage(file=self.FORM_FIELD_IMG_PATH)

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
            375.0, 231.0,
            image=self.background_img
        )

        self.back_arrow_btn = Button(
            image=self.back_arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.homepage
            ),
            relief="flat",
            cursor="hand2"
        )

        self.back_arrow_btn.place(
            x=33, y=48,
            width=38,
            height=38
        )

        self.scan_aruco_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_aruco_marker_detection,
            relief="flat",
            cursor="hand2"
        )

        self.scan_aruco_btn.place(
            x=521, y=340,
            width=30,
            height=31
        )

        self.update_pixel_cm_ratio = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.__try_save_ratios,
            relief="flat",
            cursor="hand2"
        )

        self.update_pixel_cm_ratio.place(
            x=521, y=190,
            width=30,
            height=31
        )

        self.pixel_form = self.canvas.create_image(
            476.5, 161.5,
            image=self.form_field_img
        )

        self.pixel_form = FormField(
            root=self.root,
            input_type=constants.DataTypes.FLOAT,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify='center'
        )

        self.pixel_form.place(
            x=450, y=153.4,
            width=53,
            height=19
        )

        self.cm_form = self.canvas.create_image(
            464.5, 190.5,
            image=self.form_field_img
        )

        self.cm_form = FormField(
            root=self.root,
            input_type=constants.DataTypes.FLOAT,
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify='center'
        )

        self.cm_form.place(
            x=438, y=182.4,
            width=53,
            height=19
        )

        self.cm_form.insert(0, 1)
        self.__try_load_ratio()

        self.aruco_area_form = self.canvas.create_image(
            444.5, 315.5,
            image=self.form_field_img
        )

        self.aruco_area_form = FormField(
            root=self.root,
            input_type=constants.DataTypes.FLOAT,
            setting="ARUCO_AREA_IN_CM",
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            justify='center'
        )

        self.aruco_area_form.place(
            x=418, y=307.4,
            width=53,
            height=19
        )

    def __try_load_ratio(self):
        try:
            self.__load_ratio()
        except FileNotFoundError:
            pass

    def __load_ratio(self):
        with open('App/Camera/ratios.json', 'r') as file:
            json_object = json.load(file)
            pixel_cm_ratio = json_object['pixel_cm_ratio']
            self.pixel_form.insert(0, (pixel_cm_ratio * 1))

    def __try_save_ratios(self):
        try:
            self.__save_ratios_in_json()
            self.to_page(page=self.homepage)
        except (ValueError, ZeroDivisionError):
            print("failed")
            pass

    def __save_ratios_in_json(self):
        pixel_cm_ratio, pixel_cm_squared_ratio = self.get_ratios()
        with open("App/Camera/ratios.json", 'w') as file:
            json_data = json.dumps(
                {
                    "pixel_cm_squared_ratio": pixel_cm_squared_ratio,
                    "pixel_cm_ratio": pixel_cm_ratio
                },
                indent=4
            )
            file.write(json_data)

    def get_ratios(self):
        pixel = float(self.pixel_form.get())
        cm = float(self.cm_form.get())
        pixel_cm_ratio = pixel / cm
        pixel_cm_squared_ratio = pow(pixel_cm_ratio, 2)
        return pixel_cm_ratio, pixel_cm_squared_ratio

    def start_aruco_marker_detection(self):
        if float(self.aruco_area_form.get()) > 0:
            self.aruco_area_form.update_setting()
            aruco_detector = ArucoDetector(callback_on_save=lambda: self.to_page(page=self.homepage))
            aruco_detector.start()
        else:
            self.aruco_area_form.override_text(1)
