import cv2
from decouple import config

from App.statistics_analyzer import StatisticsAnalyzer


class Shape:
    CENTER_BOUNDARY_PIXELS = int(config('CENTER_BOUNDARY_PIXELS'))

    areas = []
    area_raised_deviations = []
    perimeters = []
    perim_raised_deviations = []
    average_area = 0
    average_perim = 0

    def __init__(self, x_center, y_center, contour):
        self.x_center = x_center
        self.y_center = y_center
        self.contour = contour

    def try_add_area(self, area, cx, cy):
        if self.shape_respects_boundaries(cx, cy):
            self.areas.append(area)

    def try_add_perim(self, perim, cx, cy):
        if self.shape_respects_boundaries(cx, cy):
            self.perimeters.append(perim)

    def shape_respects_boundaries(self, cx, cy):
        if self.x_center - self.CENTER_BOUNDARY_PIXELS < cx < self.x_center + self.CENTER_BOUNDARY_PIXELS:
            if self.y_center - self.CENTER_BOUNDARY_PIXELS < cy < self.y_center + self.CENTER_BOUNDARY_PIXELS:
                return True
            return False
        return False

    def calc_average_area(self):
        statistics_analyzer = StatisticsAnalyzer(self.area_raised_deviations, self.areas)
        statistics_analyzer.try_clean_values()
        self.average_area = statistics_analyzer.get_average_value()

    def calc_average_perim(self):
        statistics_analyzer = StatisticsAnalyzer(self.perim_raised_deviations, self.perimeters)
        statistics_analyzer.try_clean_values()
        self.average_perim = statistics_analyzer.get_average_value()

    def get_shape_bounding_box_data(self):
        if self.average_perim == 0:
            self.calc_average_perim()
        if self.average_area == 0:
            self.calc_average_area()
        approx = cv2.approxPolyDP(self.contour, 0.02 * self.average_perim, True)
        x, y, w, h = cv2.boundingRect(approx)
        return x, y, w, h
