import cv2
import abc


class InputTypeInterface:
    __metaclass__ = abc.ABCMeta

    @staticmethod
    @abc.abstractmethod
    def initialize_capture(source_path, settings_address):
        pass

    @staticmethod
    @abc.abstractmethod
    def read(data):
        pass


class Video(InputTypeInterface):
    @staticmethod
    def initialize_capture(source_path, settings_address):
        cap = cv2.VideoCapture(0)
        if settings_address is not '':
            cap.open(settings_address)
        return cap

    @staticmethod
    def read(camera):
        success, img = camera.read()
        return img


class Image(InputTypeInterface):
    @staticmethod
    def initialize_capture(source_path, settings_address):
        img = cv2.imread(source_path)
        return img

    @staticmethod
    def read(img):
        return img
