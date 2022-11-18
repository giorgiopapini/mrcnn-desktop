import time
import serial
from serial import SerialException

import constants
from statistics_analyzer import StatisticsAnalyzer


class DistanceSensor:
    arduino = None

    distance_raised_deviations = []
    distances = []
    average_distance = 0

    def __init__(self, port_name):
        self.port_name = port_name
        self.try_connecting_to_arduino()

    def try_connecting_to_arduino(self):
        try:
            self.arduino = serial.Serial(self.port_name, 9600)
        except SerialException:
            print("[ERRORE] => Arduino non connesso!")

    def calc_distance(self):
        self.get_raw_distances()
        statistics_analyzer = StatisticsAnalyzer(self.distance_raised_deviations, self.distances)
        statistics_analyzer.try_clean_values()
        self.average_distance = statistics_analyzer.get_average_value()

    def get_raw_distances(self):
        t_end = time.time() + constants.SCAN_TIME
        while time.time() < t_end:
            line = self.arduino.readline()
            if line:
                string = line.decode()
                num = float(string)
                self.distances.append(num)
