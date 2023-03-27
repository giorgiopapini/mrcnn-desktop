import cv2
import numpy as np

from App.UI.Common.DetectionInputTypes import Image
from App.UI.Common.SettingsDecoder import SettingsDecoder
import json


class ArucoImageDetector:
    aruco_area_pixel = None
    is_aruco_located = False
    pixel_cm_squared_ratio = 0
    pixel_cm_ratio = 0

    def __init__(self, callback_on_save=None):
        self.callback_on_save = callback_on_save

    def start(self, img_path):
        img = cv2.imread(img_path)
        img = Image.resize(img)
        self.__try_locate_aruco_marker(img)
        if self.is_aruco_located:
            self.__save_ratios_in_json()

    def __try_locate_aruco_marker(self, img):
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        try:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
            internal_corners = np.int0(corners)
            cv2.polylines(img, internal_corners, True, (0, 255, 0), 2)
            self.aruco_area_pixel = cv2.contourArea(corners[0], True)
            self.aruco_perim_pixel = cv2.arcLength(corners[0], True)

            self.pixel_cm_squared_ratio = self.aruco_area_pixel / SettingsDecoder['ARUCO_AREA_IN_CM']
            self.pixel_cm_ratio = self.aruco_perim_pixel / SettingsDecoder['ARUCO_PERIM_IN_CM']
            self.is_aruco_located = True
        except IndexError:
            self.is_aruco_located = False

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

        self.callback_on_save()
