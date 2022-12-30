from tkinter import *

import json
import constants
import cv2

from App.Camera.PictureTaker import PictureTaker
from App.Camera.camera_object import Camera
from App.ShapeDetection.shape import Shape
from App.UI.Common.SettingsDecoder import SettingsDecoder
from App.ShapeDetection.mrcnn.mrcmm_executor import MRCNNExecutor


class MRCNNShapeDetector:
    def __init__(self, input_type=constants.DetectionInputType.VIDEO, img_path=""):
        self.input_type = input_type.value
        self.cap = self.input_type.initialize_capture(img_path, SettingsDecoder['ADDRESS'])

        self.SCAN_CHAR = SettingsDecoder['SCAN_CHAR']
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']

        self.img = None
        self.img_contour = None
        self.mask = None

        self.pixel_cm_squared_ratio = 0
        self.pixel_cm_ratio = 0

        self.shapes = []

        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.__try_load_ratios()
        self.__capture_img()
        self.__execute_mask_rcnn()

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

    def __execute_mask_rcnn(self):
        resized_img = self.__get_resized_img_to_mrcnn_required_size()
        mrcnn_executor = MRCNNExecutor(img=resized_img)
        mrcnn_executor.generate_and_save_mask()
        raw_mask = mrcnn_executor.get_saved_mask()
        self.mask = self.__get_resized_mask_to_original_size(raw_mask)

    def __get_resized_mask_to_original_size(self, mask):
        height = self.img.shape[0]
        width = self.img.shape[1]
        size = height if height > width else width
        return cv2.resize(mask, (size, size))

    def __get_resized_img_to_mrcnn_required_size(self):
        height = self.img.shape[0]
        width = self.img.shape[1]
        new_img = None
        if height > width:
            delta = height - width
            new_img = cv2.copyMakeBorder(self.img, 0, 0, 0, delta, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        else:
            delta = width - height
            new_img = cv2.copyMakeBorder(self.img, 0, delta, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        return cv2.resize(new_img, (constants.MRCNN_SIZE, constants.MRCNN_SIZE))

    def start(self):
        if self.img is None:
            cv2.destroyAllWindows()
            return False
        else:
            while True:
                self.img_contour = self.img.copy()
                self.__write_commands()
                self.get_contours()
                cv2.imshow(constants.SHAPE_DETECTION_WINDOW_NAME, self.img_contour)

                key = self.get_pressed_key()
                if key == self.SCAN_CHAR:
                    cv2.destroyAllWindows()
                    return True
                elif key == self.QUIT_CHAR:
                    cv2.destroyAllWindows()
                    return False
                elif cv2.getWindowProperty(constants.SHAPE_DETECTION_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                    return False

    def __write_commands(self):
        cv2.putText(
            self.img_contour,
            f"Premi '{self.SCAN_CHAR}' per salvare i dati",
            (20, 20),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            self.img_contour,
            f"Premi '{self.QUIT_CHAR}' per uscire",
            (20, 45),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

    def get_contours(self):
        contours, hierachy = cv2.findContours(self.mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)  # RETR_CCOMP
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            m = cv2.moments(cnt)
            if m['m00'] != 0:
                cx = int(m['m10'] / m['m00'])
                cy = int(m['m01'] / m['m00'])
                self.__update_shapes(cnt, area, peri, cx, cy)
                cv2.drawContours(self.img_contour, cnt, -1, (255, 0, 255), 2)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                padding = SettingsDecoder['PADDING_PIXELS']
                cv2.rectangle(
                    self.img_contour,
                    (x - padding, y - padding),
                    (x + w + padding, y + h + padding),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    self.img_contour,
                    f"x({cx}), y({cy})",
                    (cx - 20, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 120, 255),
                    2
                )

                cv2.putText(
                    self.img_contour,
                    "Area: " + str(int(area)),
                    (x + w + 20, y + 45),
                    cv2.FONT_HERSHEY_COMPLEX,
                    .7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    self.img_contour,
                    "Peri: " + str(int(peri)),
                    (x + w + 20, y + 70),
                    cv2.FONT_HERSHEY_COMPLEX,
                    .7,
                    (0, 255, 0),
                    2
                )

                area_cm, perim_cm = self.__try_get_area_and_perim_in_cm(area, peri)

                cv2.putText(
                    self.img_contour,
                    f"Area cm: {area_cm}",
                    (x + w + 20, y + 95),
                    cv2.FONT_HERSHEY_COMPLEX,
                    .7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    self.img_contour,
                    f"Perim cm: {perim_cm}",
                    (x + w + 20, y + 120),
                    cv2.FONT_HERSHEY_COMPLEX,
                    .7,
                    (0, 255, 0),
                    2
                )

    def __update_shapes(self, contour, area, perim, cx, cy):
        shape = self.__get_shape_if_exist(cx, cy)
        if shape is None:
            shape = Shape(cx, cy, contour)
            self.shapes.append(shape)
        shape.try_add_area(area, cx, cy)
        shape.try_add_perim(perim, cx, cy)

    def __get_shape_if_exist(self, cx, cy):
        for shape in self.shapes:
            if shape.shape_respects_boundaries(cx, cy):
                return shape
        return None

    def __try_get_area_and_perim_in_cm(self, area_pixel, perimeter_pixel):
        area = None
        perim = None
        try:
            area, perim = self.__get_area_and_perim_cm(area_pixel, perimeter_pixel)
        except ZeroDivisionError:
            area = 'undefined'
            perim = 'undefined'
        return area, perim

    def __get_area_and_perim_cm(self, area, perimeter):
        if self.pixel_cm_ratio != 'undefined' and self.pixel_cm_squared_ratio != 'undefined':
            raw_area = self.calculate_cm_from_ratio(area, self.pixel_cm_squared_ratio)
            raw_perimeter = self.calculate_cm_from_ratio(perimeter, self.pixel_cm_ratio)
            area_in_cm = format(raw_area, '.3f')
            perimeter = format(raw_perimeter, '.3f')
            return area_in_cm, perimeter
        return 'undefined', 'undefined'

    @staticmethod
    def calculate_cm_from_ratio(pixels, pixel_cm_ratio):
        return pixels / pixel_cm_ratio

    def get_pressed_key(self):
        keys = cv2.waitKey(1) & 0xFF

        if keys == ord(self.SCAN_CHAR) or keys == ord(self.SCAN_CHAR.upper()):
            return self.SCAN_CHAR
        elif keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
            return self.QUIT_CHAR
