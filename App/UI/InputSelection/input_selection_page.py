from tkinter import *

import constants
from App.ShapeDetection.cropper import Cropper
from App.UI.Recap.recap_page import RecapPage
from App.UI.page import Page


class InputSelectionPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/InputSelection/background.png"
    SCAN_BTN_IMG_PATH = "App/UI/ScanSelection/scan_btn.png"
    BACK_ARROW_IMG_PATH = "App/UI/Settings/back_arrow.png"
    PATH_FORM_IMG_PATH = "App/UI/InputSelection/path_form_img.png"

    def __init__(self, root, detector_class=None, **kwargs):
        super().__init__(root, **kwargs)
        self.detector_class = detector_class

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.scan_btn_img = PhotoImage(file=self.SCAN_BTN_IMG_PATH)
        self.back_arrow_img = PhotoImage(file=self.BACK_ARROW_IMG_PATH)
        self.path_form_img = PhotoImage(file=self.PATH_FORM_IMG_PATH)

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
                page=self.previous_page,
                homepage=self.homepage
            ),
            relief="flat",
            cursor="hand2"
        )

        self.back_arrow_btn.place(
            x=33, y=48,
            width=38,
            height=38
        )

        self.scan_from_img_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start_scanning(
                input_type=constants.DetectionInputType.IMAGE,
                img_path=self.img_path_form.get()
            ),
            relief="flat",
            cursor="hand2"
        )

        self.scan_from_img_btn.place(
            x=333, y=269,
            width=30,
            height=31
        )

        self.scan_from_camera_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.start_scanning(
                input_type=constants.DetectionInputType.VIDEO,
            ),
            relief="flat",
            cursor="hand2"
        )

        self.scan_from_camera_btn.place(
            x=704, y=269,
            width=30,
            height=31
        )

        self.img_path_form = self.canvas.create_image(
            186.0, 272.5,
            image=self.path_form_img
        )

        self.img_path_form = Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0
        )

        self.img_path_form.place(
            x=80, y=262,
            width=212,
            height=19
        )

    def btn_clicked(self):
        pass

    def start_scanning(self, input_type=constants.DetectionInputType.VIDEO, img_path=""):
        object_detector = self.detector_class(input_type=input_type, img_path=img_path)
        status = object_detector.start()
        self.get_results_and_go_to_recap_page(object_detector, status)

    def get_results_and_go_to_recap_page(self, object_detector, status):
        if status is True:
            for shape in object_detector.shapes:
                print(f"area: {shape.average_area / object_detector.pixel_cm_squared_ratio}")
                print(f"perimeter: {shape.average_perim / object_detector.pixel_cm_ratio}")
                print("================")

            cropped_images = self.crop_shapes(object_detector.img, object_detector.shapes)
            self.to_page(
                page=RecapPage,
                previous_page=self.previous_page,
                homepage=self.homepage,
                cropped_images=cropped_images
            )

    def crop_shapes(self, original_img, shapes):
        cropper = Cropper(original_img, shapes)
        return cropper.get_cropped_shapes()
