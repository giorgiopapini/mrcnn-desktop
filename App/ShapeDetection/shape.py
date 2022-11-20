from App.statistics_analyzer import StatisticsAnalyzer


class Shape:
    areas = []
    area_raised_deviations = []
    perimeters = []
    perim_raised_deviations = []
    average_area = 0
    average_perim = 0

    def __init__(self, x_center, y_center):
        self.x_center = x_center
        self.y_center = y_center

    def try_add_area(self, area, cx, cy):
        if self.__shape_respects_boundaries(cx, cy):
            self.areas.append(area)

    def try_add_perim(self, perim, cx, cy):
        if self.__shape_respects_boundaries(cx, cy):
            self.perimeters.append(perim)

    def __shape_respects_boundaries(self, cx, cy):
        if self.x_center - 10 < cx < self.x_center + 10:
            if self.y_center - 10 < cy < self.y_center + 10:
                return True
        return False

    def calc_average_area(self):
        statistics_analyzer = StatisticsAnalyzer(self.area_raised_deviations, self.areas)
        statistics_analyzer.try_clean_values()
        self.average_area = statistics_analyzer.get_average_value()

    def calc_average_perim(self):
        statistics_analyzer = StatisticsAnalyzer(self.perim_raised_deviations, self.perimeters)
        statistics_analyzer.try_clean_values()
        self.average_perim = statistics_analyzer.get_average_value()
