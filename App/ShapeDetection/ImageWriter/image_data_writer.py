from datetime import datetime
import cv2

from App.ShapeDetection.ImageWriter.final_shape import FinalShape
from App.ShapeDetection.WoundRanking.ranking import Ranking


class DataWriter:
    def __init__(self, cropped_shapes):
        self.cropped_shapes = cropped_shapes

    def get_final_shapes(self):
        final_shapes = []
        for i in range(len(self.cropped_shapes)):
            written_img = self.__try_get_written_shape(self.cropped_shapes[i])
            final_shapes.append(
                (written_img, f"{datetime.now()} ({i + 1})")
            )
        return final_shapes

    def __try_get_written_shape(self, cropped_shape):
        area_cm = cropped_shape.area
        perim_cm = cropped_shape.perim
        valutation = Ranking.get_valutation_from_area(area_cm)

        written_img = self.add_data_to_img(area_cm, perim_cm, valutation, cropped_shape.cropped_img)
        final_shape = FinalShape(area_cm, perim_cm, valutation, written_img)
        return final_shape

    def add_data_to_img(self, area, perim, valutation, cropped_img):
        data_img = cv2.copyMakeBorder(cropped_img, 100, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        cv2.putText(
            data_img,
            f"Area: {area} cm^2",
            (20, 25),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            data_img,
            f"Perimetro: {perim} cm",
            (20, 55),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            data_img,
            f"Valutazione: {valutation}",
            (20, 85),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (0, 255, 0),
            2
        )

        return data_img
