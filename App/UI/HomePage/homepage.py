from tkinter import *
from App.ArucoDetection.aruco_detection import ArucoDetector
from App.CameraCalibration.calibration import Calibrator
from App.UI.Common.SettingsDecoder import SettingsDecoder
from App.UI.ScanSelection.scan_selection_page import ScanSelectionPage
from App.UI.Settings.settings_page import SettingsPage
from App.UI.page import Page


class HomePage(Page):
    BACKGROUND_IMG_PATH = "App/UI/HomePage/background.png"
    BUTTON_IMG_PATH = "App/UI/HomePage/button_img.png"
    SETTINGS_BTN_IMG = "App/UI/HomePage/settings_btn.png"

    available = True

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.button_img = PhotoImage(file=self.BUTTON_IMG_PATH)
        self.settings_btn_img = PhotoImage(file=self.SETTINGS_BTN_IMG)

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

        self.aruco_btn = Button(
            image=self.button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_aruco_marker_detection if self.available else print(self.available),
            relief="flat",
            cursor="hand2"
        )

        self.aruco_btn.place(
            x=130, y=293,
            width=90,
            height=39
        )

        self.obj_detection_btn = Button(
            image=self.button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=ScanSelectionPage,
                previous_page=HomePage
            ),
            relief="flat",
            cursor="hand2"
        )

        self.obj_detection_btn.place(
            x=353, y=293,
            width=90,
            height=39
        )

        self.calibration_btn = Button(
            image=self.button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_calibration if self.available else None,
            relief="flat",
            cursor="hand2"
        )

        self.calibration_btn.place(
            x=576, y=293,
            width=90,
            height=39
        )

        self.settings_btn = Button(
            image=self.settings_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=SettingsPage,
                previous_page=HomePage
            ),
            relief="flat",
            cursor="hand2"
        )

        self.settings_btn.place(
            x=674, y=441,
            width=118,
            height=31
        )

    def start_aruco_marker_detection(self):
        aruco_detector = ArucoDetector()
        aruco_detector.start()

    def start_calibration(self):
        cols = SettingsDecoder['CHESSBOARD_COLS']
        rows = SettingsDecoder['CHESSBOARD_ROWS']
        cal = Calibrator(rows_num=rows, cols_num=cols)
        cal.capture_images()
        #cal.calibrate()
