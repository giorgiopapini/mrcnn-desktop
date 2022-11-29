import json
import time
import cv2

import constants
from App.Camera.camera_object import Camera
from App.ShapeDetection.shape import Shape
from App.UI.Common.SettingsDecoder import SettingsDecoder


def empty(a):
    pass


class ObjectDetector:
    undistorted_img = None

    countdown_state = False
    current_time = None
    img_contour = None

    pixel_cm_squared_ratio = 0
    pixel_cm_ratio = 0

    total_area_pixel = 0
    total_perimeter_pixel = 0

    shapes = []

    def __init__(self):
        self.SCAN_CHAR = SettingsDecoder['SCAN_CHAR']
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']
        self.countdown_value = SettingsDecoder['SCAN_TIME']

        self.current_time = time.time()

        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.cap = cv2.VideoCapture(0)
        self.cap.open(SettingsDecoder['ADDRESS'])  # registra i dati dalla webcam del telefono
        self.__try_load_ratios()
        self.__create_parameters_window()

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

    def __create_parameters_window(self):
        cv2.namedWindow(constants.PARAMETERS_WINDOW_NAME)
        cv2.resizeWindow(constants.PARAMETERS_WINDOW_NAME, 700, 315)
        cv2.createTrackbar("Threshold1", constants.PARAMETERS_WINDOW_NAME, 46, 255, empty)
        cv2.createTrackbar("Threshold2", constants.PARAMETERS_WINDOW_NAME, 46, 255, empty)
        cv2.createTrackbar("Area Min", constants.PARAMETERS_WINDOW_NAME, 5000, 30000, empty)
        cv2.createTrackbar("Area Max", constants.PARAMETERS_WINDOW_NAME, 300000, 30000, empty)
        cv2.createTrackbar("Perim Min", constants.PARAMETERS_WINDOW_NAME, 0, 10000, empty)
        cv2.createTrackbar("Perim Max", constants.PARAMETERS_WINDOW_NAME, 10000, 10000, empty)

    def start(self):
        while True:
            success, img = self.cap.read()
            self.undistorted_img = cv2.undistort(
                img,
                self.camera.camera_matrix,
                self.camera.distortion_data,
                None,
                self.camera.undistorted_camera_matrix
            )
            self.undistorted_img = cv2.resize(self.undistorted_img, None, None, fx=0.5, fy=0.5)

            img_blur = cv2.GaussianBlur(self.undistorted_img, (7, 7), 1)
            img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

            threshold1 = cv2.getTrackbarPos("Threshold1", constants.PARAMETERS_WINDOW_NAME)
            threshold2 = cv2.getTrackbarPos("Threshold2", constants.PARAMETERS_WINDOW_NAME)
            #img_canny = cv2.Canny(img_gray, threshold1, threshold2)
            img_thresh = cv2.threshold(img_gray, threshold1, threshold2, cv2.THRESH_BINARY_INV)[1]

            #cv2.imshow('canny', img_canny)
            cv2.imshow('Thresh', img_thresh)

            self.img_contour = self.undistorted_img.copy()
            self.__try_show_commmands(img=self.img_contour)
            self.__try_manage_countdown(img=self.img_contour)
            self.get_contours(img_thresh, self.img_contour)

            cv2.imshow(constants.SHAPE_DETECTION_WINDOW_NAME, self.img_contour)  # renderizza l'immagine

            if self.get_pressed_key() == self.QUIT_CHAR:
                cv2.destroyWindow(constants.PARAMETERS_WINDOW_NAME)
                cv2.destroyWindow(constants.SHAPE_DETECTION_WINDOW_NAME)
                break
            elif cv2.getWindowProperty(constants.SHAPE_DETECTION_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyWindow(constants.PARAMETERS_WINDOW_NAME)
                break
            elif cv2.getWindowProperty(constants.PARAMETERS_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyWindow(constants.SHAPE_DETECTION_WINDOW_NAME)
                break

    def __try_show_commmands(self, img):
        if not self.countdown_state:
            cv2.putText(
                img,
                f"Premi '{self.SCAN_CHAR}' per avviare la scansione",
                (20, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )
            cv2.putText(
                img,
                f"Premi '{self.QUIT_CHAR}' per uscire",
                (20, 45),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )

    def __try_manage_countdown(self, img):
        if self.countdown_state and self.countdown_value > 0:
            self.__try_decrease_countdown()
            cv2.putText(
                img,
                f"Countdown: {self.countdown_value}",
                (20, 32),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )
        elif self.countdown_value == 0:
            cv2.putText(
                img,
                f"Scansione completata! (premi '{self.QUIT_CHAR}' per i risultati)",
                (20, 32),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (0, 255, 0),
                2
            )

    def __try_decrease_countdown(self):
        if time.time() - self.current_time >= 1:
            self.current_time = time.time()
            self.countdown_value -= 1

    def get_contours(self, img, img_contour):
        contours, hierachy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)  #RETR_CCOMP
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            m = cv2.moments(cnt)
            if m['m00'] != 0:
                cx = int(m['m10'] / m['m00'])
                cy = int(m['m01'] / m['m00'])
                if self.__contour_respect_trackbars_conditions(area, peri):
                    self.__try_update_shapes(cnt, area, peri, cx, cy)
                    cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 7)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    x, y, w, h = cv2.boundingRect(approx)
                    cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 5)

                    cv2.putText(
                        img_contour,
                        f"x({cx}), y({cy})",
                        (cx - 20, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 120, 255),
                        2
                    )

                    cv2.putText(
                        img_contour,
                        "Area: " + str(int(area)),
                        (x + w + 20, y + 45),
                        cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        img_contour,
                        "Peri: " + str(int(peri)),
                        (x + w + 20, y + 70),
                        cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0),
                        2
                    )

                    area_cm, perim_cm = self.__try_get_area_and_perim_in_cm(area, peri)

                    cv2.putText(
                        img_contour,
                        f"Area cm: {area_cm}",
                        (x + w + 20, y + 95),
                        cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        img_contour,
                        f"Perim cm: {perim_cm}",
                        (x + w + 20, y + 120),
                        cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0),
                        2
                    )

    def __contour_respect_trackbars_conditions(self, area, perimeter):
        min_area_selected = cv2.getTrackbarPos("Area Min", constants.PARAMETERS_WINDOW_NAME)
        max_area_selected = cv2.getTrackbarPos("Area Max", constants.PARAMETERS_WINDOW_NAME)
        min_peri_selected = cv2.getTrackbarPos("Perim Min", constants.PARAMETERS_WINDOW_NAME)
        max_peri_selected = cv2.getTrackbarPos("Perim Max", constants.PARAMETERS_WINDOW_NAME)

        if min_area_selected < area < max_area_selected:
            if min_peri_selected < perimeter < max_peri_selected:
                return True
        return False

    def __try_update_shapes(self, contour, area, perim, cx, cy):
        if self.countdown_state and self.countdown_value > 0:
            self.__update_shapes(contour, area, perim, cx, cy)

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

        if keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
            if self.countdown_value == 0:
                self.__obtain_results()
                return self.QUIT_CHAR
            elif self.countdown_state is False:
                return self.QUIT_CHAR
        elif keys == ord(self.SCAN_CHAR) or keys == ord(self.SCAN_CHAR.upper()):
            if self.pixel_cm_squared_ratio != 'undefined' and self.pixel_cm_ratio != 'undefined':
                self.__try_start_countdown()

    def __obtain_results(self):
        areas = []
        perimeters = []
        for shape in self.shapes:
            shape.calc_average_area()
            areas.append(shape.average_area)
            shape.calc_average_perim()
            perimeters.append(shape.average_perim)
        self.total_area_pixel = sum(areas)
        self.total_perimeter_pixel = sum(perimeters)

    def __try_start_countdown(self):
        if self.countdown_state is False:
            self.countdown_state = True
