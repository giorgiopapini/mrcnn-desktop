import cv2
from datetime import datetime

from App.UI.Common.SettingsDecoder import SettingsDecoder


class Cropper:
    def __init__(self, original_img, shapes):
        self.PADDING_PIXELS = SettingsDecoder['PADDING_PIXELS']
        self.original_img = original_img
        self.shapes = shapes

    def crop_shapes(self):
        for shape in self.shapes:
            cropped_img = self.__try_get_cropped_shape(shape)
            self.__save_img(cropped_img)

    def __try_get_cropped_shape(self, shape):
        img = self.original_img.copy()
        x, y, w, h = shape.get_shape_bounding_box_data()
        return img[
               (y - self.PADDING_PIXELS):(y + h + self.PADDING_PIXELS),
               (x - self.PADDING_PIXELS):(x + w + self.PADDING_PIXELS)
               ]

    def __save_img(self, cropped_img):
        cv2.imshow(f"{datetime.now()}", cropped_img)

