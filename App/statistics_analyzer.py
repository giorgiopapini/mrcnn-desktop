
class StatisticsAnalyzer:
    def __init__(self, raised_deviations, values):
        self.raised_deviations = raised_deviations
        self.values = values

    def try_clean_values(self):
        try:
            self.clean_values()
        except ZeroDivisionError:
            print("[ERRORE] => La lista non presenta alcun valore")

    def clean_values(self):
        raw_average = self.__calc_average(array=self.values)
        variance = self.__calc_variance(average=raw_average)
        self.__del_values_with_deviations_greater_than_variance(variance=variance)

    def __calc_average(self, array):
        elements_sum = 0
        for num in array:
            elements_sum += num
        return elements_sum / len(array)

    def __calc_variance(self, average):
        deviations_sum = 0
        for num in self.values:
            deviation = (num - average) ** 2
            self.raised_deviations.append(deviation)
            deviations_sum += deviation

        return deviations_sum / len(self.values)

    def __del_values_with_deviations_greater_than_variance(self, variance):
        try:
            for i in range(len(self.raised_deviations)):
                if self.raised_deviations[i] > variance:
                    self.values.pop(i)
        except IndexError:
            pass

    def get_average_value(self):
        try:
            return self.__calc_average(array=self.values)
        except ZeroDivisionError:
            return 0
