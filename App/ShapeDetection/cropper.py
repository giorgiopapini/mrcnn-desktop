from datetime import datetime

import cv2

import constants
from App.ShapeDetection.cropped_shape import CroppedShape
from App.UI.Common.SettingsDecoder import SettingsDecoder


class Cropper:
    def __init__(self, original_img, shapes):
        self.PADDING_PIXELS = SettingsDecoder['PADDING_PIXELS']
        self.original_img = original_img
        self.shapes = shapes

    def get_cropped_shapes(self):
        cropped_shapes = []
        for i in range(len(self.shapes)):
            cropped_shape = self.__try_get_cropped_shape(self.shapes[i])
            cropped_shapes.append(
                (cropped_shape, f"{datetime.now()} ({i + 1})")
            )
        return cropped_shapes

    def __try_get_cropped_shape(self, shape):
        img = self.original_img.copy()
        x, y, w, h = shape.get_shape_bounding_box_data()
        img_height = img.shape[0]
        img_width = img.shape[1]
        cropped_img = img[
               (y - self.PADDING_PIXELS if y - self.PADDING_PIXELS > 0 else y)
               :(y + h + self.PADDING_PIXELS if y + h + self.PADDING_PIXELS < img_height else y + h),
               (x - self.PADDING_PIXELS if x - self.PADDING_PIXELS > 0 else x)
               :(x + w + self.PADDING_PIXELS if x + w + self.PADDING_PIXELS < img_width else x + h)
               ]
        cropped_img = self.get_resized_cropped_img(cropped_img)
        cropped_shape = CroppedShape(shape.average_area, shape.average_perim, cropped_img)

        return cropped_shape

    def get_resized_cropped_img(self, cropped_img):
        height = cropped_img.shape[0]
        width = cropped_img.shape[1]
        if height > width:
            return self.get_resized_img_by_height(cropped_img, height, width)
        return self.get_resized_img_by_width(cropped_img, height, width)

    def get_resized_img_by_height(self, img=None, height=None, width=None):
        new_height = constants.CONST_HEIGHT
        new_width = (width * new_height) / height
        dim = (int(new_width), int(new_height))
        resized = cv2.resize(img, dim)
        return resized

    def get_resized_img_by_width(self, img=None, heigth=None, width=None):
        new_width = constants.CONST_WIDTH
        new_height = (heigth * new_width) / width
        dim = (int(new_width), int(new_height))
        resized = cv2.resize(img, dim)
        return resized
