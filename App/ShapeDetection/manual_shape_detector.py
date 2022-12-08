import json
import cv2
from tkinter import *

import numpy as np

import constants
from App.Camera.PictureTaker import PictureTaker
from App.Camera.camera_object import Camera
from App.UI.Common.SettingsDecoder import SettingsDecoder


class ManualShapeDetector:
    def __init__(self, input_type=constants.DetectionInputType.VIDEO, img_path=""):
        self.input_type = input_type.value
        self.cap = self.input_type.initialize_capture(img_path, SettingsDecoder['ADDRESS'])

        self.SCAN_CHAR = SettingsDecoder['SCAN_CHAR']
        self.ERASE_CHAR = SettingsDecoder['ERASE_CHAR']
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']

        self.img = None
        self.contours = [[]]
        self.current_contour = 0
        self.current_point = None

        self.pixel_cm_squared_ratio = 0
        self.pixel_cm_ratio = 0

        self.total_area_pixel = 0
        self.total_perimeter_pixel = 0

        self.shapes = []

        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.__try_load_ratios()
        self.__capture_img()

    def __try_load_ratios(self):
        try:
            self.__load_ratios()
        except FileNotFoundError:
            self.pixel_cm_ratio = 'undefined'
            self.pixel_cm_squared_ratio = 'undefined'

    def __load_ratios(self):
        with open('App/Camera/ratios.json', 'r') as file:
            json_object = json.load(file)
            self.pixel_cm_ratio = json_object['pixel_cm_ratio']
            self.pixel_cm_squared_ratio = json_object['pixel_cm_squared_ratio']

    def __capture_img(self):
        if self.input_type == constants.DetectionInputType.IMAGE.value:
            self.img = self.cap.copy()
        else:
            picture_taker = PictureTaker()
            self.img = picture_taker.take_picture()

    def start(self):
        if self.img is None:
            cv2.destroyAllWindows()
            return False
        else:
            while True:
                self.__write_commands()
                self.__draw_lines(is_closed=False)
                self.__draw_points()
                cv2.imshow('image', self.img)
                cv2.setMouseCallback('image', self.click_event)

                key = self.get_pressed_key()
                if key == self.ERASE_CHAR:
                    self.__try_delete_last_line()
                elif key == self.SCAN_CHAR:
                    print(self.contours)
                    arr = np.array(self.contours[0])
                    area = cv2.contourArea(arr)
                    perimeter = cv2.arcLength(arr, True)
                    print(f"area: {area} ----- perim: {perimeter}")
                elif key == self.QUIT_CHAR:
                    cv2.destroyAllWindows()
                    break
                elif cv2.getWindowProperty('image', cv2.WND_PROP_VISIBLE) < 1:
                    break

    def __write_commands(self):
        cv2.putText(
            self.img,
            f"Premi '{self.SCAN_CHAR}' per salvare i dati",
            (20, 20),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            self.img,
            f"Premi '{self.ERASE_CHAR}' per cancellare",
            (20, 45),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            self.img,
            f"Premi '{self.QUIT_CHAR}' per uscire",
            (20, 70),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            self.img,
            f"Usa il tasto sinistro del mouse per tracciare le linee",
            (20, 95),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            self.img,
            f"Usa il tasto destro del mouse per terminare la stesura di un contorno",
            (20, 120),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

    def __draw_lines(self, is_closed):
        for contour in self.contours:
            pts = np.array(contour, np.int32)
            pts = pts.reshape((-1, 1, 2))
            color = (0, 255, 0)
            thickness = 3
            self.img = cv2.polylines(self.img, [pts], is_closed, color, thickness)

    def __draw_points(self):
        for contour in self.contours:
            for point in contour:
                x = point[0]
                y = point[1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(self.img, f"({x}, {y})", (x, y), font, .6, (255, 0, 0), 2)

    def __try_delete_last_line(self):
        try:
            self.contours[self.current_contour] = self.contours[self.current_contour][:-2]
            self.current_point = self.contours[self.current_contour][len(self.contours[self.current_contour]) - 1]
        except IndexError:
            self.current_point = None

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__save_point((x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            cnt = self.contours[self.current_contour]
            if len(cnt) > 2:
                start_x = cnt[0][0]
                start_y = cnt[0][1]
                self.__save_point((start_x, start_y))
                self.__save_contour_and_create_new()

        elif event == cv2.EVENT_MOUSEMOVE:
            pass

    def __save_point(self, point):
        if self.current_point is None:
            self.current_point = point
        else:
            self.contours[self.current_contour].append(self.current_point)
            self.contours[self.current_contour].append(point)
            self.current_point = point

    def __save_contour_and_create_new(self):
        if len(self.contours[self.current_contour]) > 2:
            self.contours.append([])
            self.current_point = None
            self.current_contour += 1

    def get_pressed_key(self):
        keys = cv2.waitKey(1) & 0xFF

        if keys == ord(self.ERASE_CHAR) or keys == ord(self.ERASE_CHAR.upper()):
            return self.ERASE_CHAR
        elif keys == ord(self.SCAN_CHAR) or keys == ord(self.SCAN_CHAR.upper()):
            return self.SCAN_CHAR
        elif keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
            return self.QUIT_CHAR
