from tkinter import *

from App.ShapeDetection.cropper import Cropper
from App.UI.Recap.recap_page import RecapPage
from App.UI.page import Page


class ScanPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/Scan/background.png"
    DELAY_MILLISECONDS = 100

    def __init__(self, root, object_detector=None, **kwargs):
        super().__init__(root, **kwargs)
        self.object_detector = object_detector

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.canvas = Canvas(
            self.root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.background = self.canvas.create_image(
            375.0, 231.0,
            image=self.background_img
        )

        self.after(self.DELAY_MILLISECONDS, self.scan)

    def scan(self):
        status = self.object_detector.try_start()
        self.get_results_and_go_to_recap_page(self.object_detector, status)

    def get_results_and_go_to_recap_page(self, object_detector, status):
        if status is True:
            cropped_shapes = self.crop_shapes(
                object_detector.img,
                object_detector.shapes,
                object_detector.pixel_cm_ratio,
                object_detector.pixel_cm_squared_ratio
            )

            self.to_page(
                page=RecapPage,
                previous_page=self.previous_page,
                homepage=self.homepage,
                cropped_shapes=cropped_shapes
            )
        else:
            self.to_page(
                page=self.previous_page,
                homepage=self.homepage
            )

    def crop_shapes(self, original_img, shapes, pixel_cm_ratio, pixel_cm_squared_ratio):
        cropper = Cropper(original_img, shapes, pixel_cm_ratio, pixel_cm_squared_ratio)
        return cropper.get_cropped_shapes()
