import abc


class ObjectDetectorInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def set_trackbars(self):
        pass

    @abc.abstractmethod
    def refine_image(self, img_blur):
        pass
