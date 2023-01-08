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

    @staticmethod
    def resize(img):
        dim = None
        (h, w) = img.shape[:2]
        desired_width = constants.FRAME_WIDTH if w > h else None
        desired_height = constants.FRAME_HEIGHT if h > w else None

        if desired_width is None and desired_height is None:
            return img

        if desired_width is None:
            r = desired_height / float(h)
            dim = (int(w * r), desired_height)
        else:
            r = desired_width / float(w)
            dim = (desired_width, int(h * r))

        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


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
        return Video.resize(img)


class Image(InputTypeInterface):
    @staticmethod
    def initialize_capture(source_path, settings_address):
        img = cv2.imread(source_path)
        return img

    @staticmethod
    def read(img, camera_matrix, distortion_data, undistorted_camera_matrix):
        return Image.resize(img)
