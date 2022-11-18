import time
import cv2
import numpy as np
import constants
from camera_object import Camera
from statistics_analyzer import StatisticsAnalyzer


def empty(a):
    pass


class ObjectDetector:
    countdown_value = constants.SCAN_TIME
    countdown_state = False
    current_time = None
    img_contour = None

    area_raised_deviations = []
    areas = []
    average_area = 0

    perim_raised_deviations = []
    perimeters = []
    average_perim = 0

    aruco_area_pixel = None
    is_aruco_located = False
    pixel_cm_squared_ratio = 0
    pixel_cm_ratio = 0

    def __init__(self):
        self.current_time = time.time()

        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.cap = cv2.VideoCapture(0)
        self.cap.open(constants.ADDRESS)  # registra i dati dalla webcam del telefono

        self.__create_parameters_window()

    def __create_parameters_window(self):
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 700, 315)
        cv2.createTrackbar("Threshold1", "Parameters", 46, 255, empty)
        cv2.createTrackbar("Threshold2", "Parameters", 46, 255, empty)
        cv2.createTrackbar("Area Min", "Parameters", 5000, 30000, empty)
        cv2.createTrackbar("Area Max", "Parameters", 300000, 30000, empty)
        cv2.createTrackbar("Perim Min", "Parameters", 0, 10000, empty)
        cv2.createTrackbar("Perim Max", "Parameters", 10000, 10000, empty)

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

            img_blur = cv2.GaussianBlur(undistorted_img, (7, 7), 1)
            img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)

            threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
            threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
            img_canny = cv2.Canny(img_gray, threshold1, threshold2)

            kernel = np.ones((5, 5))
            img_dil = cv2.dilate(img_canny, kernel, iterations=1)

            self.img_contour = undistorted_img.copy()
            self.__try_show_commmands(img=self.img_contour)
            self.__try_manage_countdown(img=self.img_contour)
            self.__try_locate_aruco_marker(img=self.img_contour)
            self.get_contours(img_dil, self.img_contour)

            cv2.imshow("Result", self.img_contour)  # renderizza l'immagine

            if self.get_pressed_key() == constants.QUIT_CHAR:
                break

    def __try_show_commmands(self, img):
        if not self.countdown_state:
            cv2.putText(
                img,
                f"Press '{constants.SCAN_CHAR}' to start scanning",
                (20, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )
            cv2.putText(
                img,
                f"Press '{constants.QUIT_CHAR}' to quit",
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
                (0, 255, 255),
                2
            )
        elif self.countdown_value == 0:
            cv2.putText(
                img,
                f"Scan Completed! (Press '{constants.QUIT_CHAR}' to get the results)",
                (20, 32),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (0, 255, 0),
                2
            )

    def __try_locate_aruco_marker(self, img):
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        try:
            (corners, ids, rejected) = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
            self.aruco_area_pixel = cv2.contourArea(corners[0], True)
            self.aruco_perim_pixel = cv2.arcLength(corners[0], True)
            self.pixel_cm_squared_ratio = self.aruco_area_pixel / constants.ARUCO_AREA_IN_CM
            self.pixel_cm_ratio = self.aruco_perim_pixel / constants.ARUCO_PERIM_IN_CM
            print(f"ARUCO REAL CORNERS: {corners}")
            cv2.putText(
                img,
                "Aruco marker localizzato!",
                (20, 70),
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
                (20, 70),
                cv2.FONT_HERSHEY_COMPLEX,
                .7,
                (0, 0, 255),
                2
            )
            self.is_aruco_located = False

    def __try_decrease_countdown(self):
        if time.time() - self.current_time >= 1:
            self.current_time = time.time()
            self.countdown_value -= 1

    def get_contours(self, img, img_contour):
        contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # IMPORTANTE!!!! -->TROVARE UN MODO PER IGNORARE IL MARKER!!!
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)

            if self.__contour_respect_trackbars_conditions(area, peri):
                cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 7)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 5)

                cv2.putText(
                    img_contour,
                    "Points: " + str(len(approx)),
                    (x + w + 20, y + 20),
                    cv2.FONT_HERSHEY_COMPLEX,
                    .7,
                    (0, 255, 0),
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

                self.__try_populate_data(current_area=area, current_perim=peri)

    def __contour_respect_trackbars_conditions(self, area, perimeter):
        min_area_selected = cv2.getTrackbarPos("Area Min", "Parameters")
        max_area_selected = cv2.getTrackbarPos("Area Max", "Parameters")
        min_peri_selected = cv2.getTrackbarPos("Perim Min", "Parameters")
        max_peri_selected = cv2.getTrackbarPos("Perim Max", "Parameters")

        if min_area_selected < area < max_area_selected:
            if min_peri_selected < perimeter < max_peri_selected:
                return True
        return False

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
        raw_area = self.calculate_cm_from_ratio(area, self.pixel_cm_squared_ratio)
        raw_perimeter = self.calculate_cm_from_ratio(perimeter, self.pixel_cm_ratio)
        area_in_cm = format(raw_area, '.3f') if self.is_aruco_located else 'undefined'
        perimeter = format(raw_perimeter, '.3f') if self.is_aruco_located else 'undefined'
        return area_in_cm, perimeter

    @staticmethod
    def calculate_cm_from_ratio(pixels, pixel_cm_ratio):
        return pixels / pixel_cm_ratio

    def __try_populate_data(self, current_area, current_perim):
        if self.countdown_state and self.countdown_value > 0:
            self.areas.append(current_area)
            self.perimeters.append(current_perim)

    def calc_area(self):
        statistics_analyzer = StatisticsAnalyzer(self.area_raised_deviations, self.areas)
        statistics_analyzer.try_clean_values()
        self.average_area = statistics_analyzer.get_average_value()

    def calc_perim(self):
        statistics_analyzer = StatisticsAnalyzer(self.perim_raised_deviations, self.perimeters)
        statistics_analyzer.try_clean_values()
        self.average_perim = statistics_analyzer.get_average_value()

    def get_pressed_key(self):
        keys = cv2.waitKey(1) & 0xFF

        if keys == ord(constants.QUIT_CHAR):
            if self.countdown_value == 0:
                self.__obtain_results()
                return constants.QUIT_CHAR
            elif self.countdown_state is False:
                return constants.QUIT_CHAR
        elif keys == ord(constants.SCAN_CHAR) and self.is_aruco_located is True:
            self.__try_start_countdown()

    def __obtain_results(self):
        self.calc_area()
        self.calc_perim()

    def __try_start_countdown(self):
        if self.countdown_state is False:
            self.countdown_state = True
