from datetime import datetime

from App.UI.Common.SettingsDecoder import SettingsDecoder


class Cropper:
    def __init__(self, original_img, shapes):
        self.PADDING_PIXELS = SettingsDecoder['PADDING_PIXELS']
        self.original_img = original_img
        self.shapes = shapes

    def get_cropped_shapes(self):
        cropped_shapes = []
        for i in range(len(self.shapes)):
            cropped_img = self.__try_get_cropped_shape(self.shapes[i])
            cropped_shapes.append(
                (cropped_img, f"{datetime.now()} ({i + 1})")
            )
        return cropped_shapes

    def __try_get_cropped_shape(self, shape):
        img = self.original_img.copy()
        x, y, w, h = shape.get_shape_bounding_box_data()
        img_height = img.shape[0]
        img_width = img.shape[1]
        return img[
               (y - self.PADDING_PIXELS if y - self.PADDING_PIXELS > 0 else y)
               :(y + h + self.PADDING_PIXELS if y + h + self.PADDING_PIXELS < img_height else y + h),
               (x - self.PADDING_PIXELS if x - self.PADDING_PIXELS > 0 else x)
               :(x + w + self.PADDING_PIXELS if x + w + self.PADDING_PIXELS < img_width else x + h)
               ]
