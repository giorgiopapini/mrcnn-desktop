import cv2

import constants
from App.ShapeDetection.basic_shape_detector import BasicShapeDetector
from App.ShapeDetection.object_detector_interface import ObjectDetectorInterface


class AdaptiveThresholdShapeDetector(BasicShapeDetector, ObjectDetectorInterface):
    def __init__(self):
        super().__init__()

    def set_trackbars(self):
        cv2.createTrackbar("Regioni", constants.PARAMETERS_WINDOW_NAME, 3, 255, constants.empty)
        cv2.createTrackbar("Threshold1", constants.PARAMETERS_WINDOW_NAME, 2, 255, constants.empty)

    def refine_image(self, img_blur):
        region_size = cv2.getTrackbarPos("Regioni", constants.PARAMETERS_WINDOW_NAME)
        threshold1 = cv2.getTrackbarPos("Threshold1", constants.PARAMETERS_WINDOW_NAME)
        img_thresh = cv2.adaptiveThreshold(
            img_blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            self.__get_corret_region_size(region_size),
            threshold1
        )
        return img_thresh

    def __get_corret_region_size(self, size):
        if size <= 2:
            return 3
        else:
            if size % 2 == 0:
                return size + 1
            return size
