import cv2
import abc

import constants


class InputTypeInterface:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def initialize_capture(source_path, settings_address):
        pass

    @staticmethod
    @abc.abstractmethod
    def read(data, camera_matrix, distortion_data, undistorted_camera_matrix):
        pass


class Video(InputTypeInterface):
    @staticmethod
    def initialize_capture(source_path, settings_address):
        cap = cv2.VideoCapture(0)
        if settings_address is not '':
            cap.open(settings_address)
        return cap

    @staticmethod
    def read(camera, camera_matrix, distortion_data, undistorted_camera_matrix):
        success, img = camera.read()
        img = cv2.undistort(
            img,
            camera_matrix,
            distortion_data,
            None,
            undistorted_camera_matrix
        )
        return img


class Image(InputTypeInterface):
    @staticmethod
    def initialize_capture(source_path, settings_address):
        img = cv2.imread(source_path)
        return img

    @staticmethod
    def read(img, camera_matrix, distortion_data, undistorted_camera_matrix):
        return img
