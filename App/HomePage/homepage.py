from tkinter import *

from App.ArucoDetection.aruco_detection import ArucoDetector
from App.CameraCalibration.calibration import Calibrator
from App.ShapeDetection.shape_detection import ObjectDetector


class HomePage:
    BACKGROUND_IMG_PATH = "App/HomePage/background.png"
    BUTTON_IMG_PATH = "App/HomePage/button_img.png"

    available = True

    def __init__(self, root):
        self.root = root
        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.button_img = PhotoImage(file=self.BUTTON_IMG_PATH)

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
            command=self.start_obj_detection if self.available else None,
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

    def start_obj_detection(self):
        self.__set_button_state(False)
        object_detector = ObjectDetector()
        object_detector.start()
        print(object_detector.average_area / object_detector.pixel_cm_squared_ratio)

    def start_aruco_marker_detection(self):
        aruco_detector = ArucoDetector()
        aruco_detector.start()

    def start_calibration(self):
        cal = Calibrator(rows_num=6, cols_num=8)
        cal.capture_images()
        #cal.calibrate()

    def __set_button_state(self, state):
        self.available = state
