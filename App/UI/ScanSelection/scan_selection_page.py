from tkinter import *

from App.ShapeDetection.adaptive_threshold_shape_detector import AdaptiveThresholdShapeDetector
from App.ShapeDetection.basic_shape_detector import BasicShapeDetector
from App.UI.InputSelection.input_selection_page import InputSelectionPage
from App.UI.page import Page


class ScanSelectionPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/ScanSelection/background.png"
    SCAN_BTN_IMG_PATH = "App/UI/ScanSelection/scan_btn.png"
    BACK_ARROW_IMG_PATH = "App/UI/Settings/back_arrow.png"

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.scan_btn_img = PhotoImage(file=self.SCAN_BTN_IMG_PATH)
        self.back_arrow_img = PhotoImage(file=self.BACK_ARROW_IMG_PATH)

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

        self.manual_scan_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.manual_scan_btn.place(
            x=349, y=189,
            width=30,
            height=31
        )

        self.canny_edge_scan_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=InputSelectionPage,
                homepage=self.homepage,
                previous_page=ScanSelectionPage,
                detector_class=BasicShapeDetector,
            ),
            relief="flat",
            cursor="hand2"
        )

        self.canny_edge_scan_btn.place(
            x=349, y=330,
            width=30,
            height=31
        )

        self.adaptive_thresholding_scan_btn = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=InputSelectionPage,
                homepage=self.homepage,
                previous_page=ScanSelectionPage,
                detector_class=AdaptiveThresholdShapeDetector,
            ),
            relief="flat",
            cursor="hand2"
        )

        self.adaptive_thresholding_scan_btn.place(
            x=653, y=330,
            width=30,
            height=31
        )

        self.mask_rcnn_scan_bnt = Button(
            image=self.scan_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_clicked,
            relief="flat",
            cursor="hand2"
        )

        self.mask_rcnn_scan_bnt.place(
            x=653, y=189,
            width=30,
            height=31
        )

    def btn_clicked(self):
        pass
