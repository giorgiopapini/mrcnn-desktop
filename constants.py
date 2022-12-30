from enum import Enum

from App.UI.Common.DataTypes import String, Char, Integer, Float
from App.UI.Common.DetectionInputTypes import Video, Image

BACKSPACE_KEYSYM_NUM = 65288
SETTINGS_FILE_NAME = "settings.json"
FRAME_HEIGHT = 540
FRAME_WIDTH = 960


# ========== CROPPED IMAGES RESIZE PROCESS ==========
CONST_WIDTH = 720
CONST_HEIGHT = 576


# ========== MRCNN MASK IMAGES SIZE ==========
MRCNN_SIZE = 224


# ========== DATA TYPES ENUM FOR FORMFIELD CLASS ==========
class DataTypes(Enum):
    STR = String
    CHAR = Char
    INT = Integer
    FLOAT = Float


class DetectionInputType(Enum):
    VIDEO = Video
    IMAGE = Image


def empty(a):
    pass


# ========== CALIBRATION ==========
SAVING_TIME = 1

# ========== PAGE NAMES ==========
ARUCO_DETECTION_WINDOW_NAME = "Aruco Scanner"
SHAPE_DETECTION_WINDOW_NAME = "Scanner"
PARAMETERS_WINDOW_NAME = "Parameters"
THRESHOLD_WINDOW_NAME = "Threshold"
CALIBRATION_WINDOW_NAME = "Camera Calibration"
PICTURE_TAKER_WINDOW_NAME = "Take a picture"
