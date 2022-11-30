from enum import Enum

from App.UI.Common.DataTypes import String, Char, Integer

BACKSPACE_KEYSYM_NUM = 65288
SETTINGS_FILE_NAME = "settings.json"


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
THRESHOLD_WINDOW_NAME = "Threshold"
CALIBRATION_WINDOW_NAME = "Camera Calibration"
