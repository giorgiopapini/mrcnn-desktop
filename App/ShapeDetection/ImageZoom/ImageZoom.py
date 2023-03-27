import cv2


class ImageZoom:
    def __init__(self, image, zoom_level=1, zoom_factor=1.1):
        self.image = image
        self.zoom_level = zoom_level
        self.zoom_factor = zoom_factor

    def zoom_in(self):
        self.zoom_level *= self.zoom_factor
        return self.__zoom()

    def zoom_out(self):
        self.zoom_level /= self.zoom_factor
        return self.__zoom()

    def __zoom(self):
        frame_width = self.image.shape[1]
        frame_height = self.image.shape[0]
        resized_image = cv2.resize(
            self.image,
            None,
            fx=self.zoom_level * self.zoom_factor,
            fy=self.zoom_level * self.zoom_factor,
            interpolation=cv2.INTER_LINEAR
        )

        x = int((resized_image.shape[1] - frame_width) / 2)
        y = int((resized_image.shape[0] - frame_height) / 2)

        zoomed_image = resized_image[y:y + frame_height, x:x + frame_width]
        return zoomed_image
