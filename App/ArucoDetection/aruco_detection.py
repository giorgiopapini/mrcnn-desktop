import json
import numpy as np
import cv2
from decouple import config

import constants
from App.Camera.camera_object import Camera


class ArucoDetector:
    SCAN_CHAR = config('SCAN_CHAR')
    QUIT_CHAR = config('QUIT_CHAR')

    aruco_area_pixel = None
    is_aruco_located = False
    pixel_cm_squared_ratio = 0
    pixel_cm_ratio = 0

    def __init__(self):
        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.cap = cv2.VideoCapture(0)
        #self.cap.open(constants.ADDRESS)  # registra i dati dalla webcam del telefono

    def start(self):
        while True:
            success, img = self.cap.read()
            undistorted_img = cv2.undistort(
                img,
                self.camera.camera_matrix,
                self.camera.distortion_data,
                None,
                self.camera.undistorted_camera_matrix
            )
            undistorted_img = cv2.resize(undistorted_img, None, None, fx=0.5, fy=0.5)

            self.__try_locate_aruco_marker(img=undistorted_img)
            self.__try_show_commands(img=undistorted_img)
            cv2.imshow(constants.ARUCO_DETECTION_WINDOW_NAME, undistorted_img)
            key_pressed = self.get_key_pressed()
            if key_pressed == self.SCAN_CHAR:
                if self.is_aruco_located:
                    cv2.destroyWindow(constants.ARUCO_DETECTION_WINDOW_NAME)
                    self.__save_ratios_in_json()
                    break
            elif key_pressed == self.QUIT_CHAR:
                cv2.destroyWindow(constants.ARUCO_DETECTION_WINDOW_NAME)
                break
            elif cv2.getWindowProperty(constants.ARUCO_DETECTION_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

    def __try_show_commands(self, img):
        cv2.putText(
            img,
            f"Premi '{self.QUIT_CHAR}' per uscire",
            (20, 45),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )
        if self.is_aruco_located:
            cv2.putText(
                img,
                f"Premi '{self.SCAN_CHAR}' per salvare",
                (20, 70),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )

    def __try_locate_aruco_marker(self, img):
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        try:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
            internal_corners = np.int0(corners)
            cv2.polylines(img, internal_corners, True, (0, 255, 0), 5)
            self.aruco_area_pixel = cv2.contourArea(corners[0], True)
            self.aruco_perim_pixel = cv2.arcLength(corners[0], True)
            self.pixel_cm_squared_ratio = self.aruco_area_pixel / constants.ARUCO_AREA_IN_CM
            self.pixel_cm_ratio = self.aruco_perim_pixel / constants.ARUCO_PERIM_IN_CM
            cv2.putText(
                img,
                "Aruco marker localizzato!",
                (20, 20),
                cv2.FONT_HERSHEY_COMPLEX,
                .7,
                (0, 255, 0),
                2
            )
            self.is_aruco_located = True
        except IndexError:
            cv2.putText(
                img,
                "Aruco marker non localizzato!",
                (20, 20),
                cv2.FONT_HERSHEY_COMPLEX,
                .7,
                (0, 0, 255),
                2
            )
            self.is_aruco_located = False

    def get_key_pressed(self):
        keys = cv2.waitKey(1) & 0xFF

        if keys == ord(self.SCAN_CHAR) or keys == ord(self.SCAN_CHAR.upper()):
            return self.QUIT_CHAR
        elif keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
            return self.QUIT_CHAR


    def __save_ratios_in_json(self):
        with open("App/Camera/ratios.json", 'w') as file:
            json_data = json.dumps(
                {
                    "pixel_cm_squared_ratio": self.pixel_cm_squared_ratio,
                    "pixel_cm_ratio": self.pixel_cm_ratio
                },
                indent=4
            )
            file.write(json_data)
