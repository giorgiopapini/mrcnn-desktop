from App.CameraCalibration.calibration import Calibrator
from App.ObjectDetection.object_detection import ObjectDetector

from new_main import new_main


def main():
    object_detector = ObjectDetector()
    object_detector.start()

    print(f"AREAS: {object_detector.areas}")
    print(f"PERIMETERS: {object_detector.perimeters}")
    print(f"AVERAGE AREA: {object_detector.average_area}")
    print(f"AVERAGE PERIM: {object_detector.average_perim}")

    real_area = object_detector.calculate_cm_from_ratio(
        object_detector.average_area,
        object_detector.pixel_cm_squared_ratio
    )

    real_perimeter = object_detector.calculate_cm_from_ratio(
        object_detector.average_perim,
        object_detector.pixel_cm_ratio
    )

    print(f"TOTAL AREA IN CM: {real_area}")
    print(f"TOTAL PERIMETER IN CM: {real_perimeter}")


def main_cal():
    cal = Calibrator(rows_num=6, cols_num=8)
    #cal.capture_images()
    cal.calibrate()


if __name__ == '__main__':
    #main_cal()
    #main()
    new_main()
