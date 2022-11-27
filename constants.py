from enum import Enum

from App.UI.Common.DataTypes import String, Char, Integer

ARUCO_AREA_IN_CM = 23  # 25 cm^2
ARUCO_PERIM_IN_CM = 19  # 20 cm

ADDRESS = "https://192.168.1.65:8080/video"

BACKSPACE_KEYSYM_NUM = 65288

# ========== DATA TYPES ENUM FOR FORMFIELD CLASS ==========
class DataTypes(Enum):
    STR = String
    CHAR = Char
    INT = Integer


# ========== CALIBRATION ==========
SAVING_TIME = 1

# ========== PAGE NAMES ==========
ARUCO_DETECTION_WINDOW_NAME = "Aruco Scanner"
SHAPE_DETECTION_WINDOW_NAME = "Scanner"
PARAMETERS_WINDOW_NAME = "Parameters"
CALIBRATION_WINDOW_NAME = "Camera Calibration"
