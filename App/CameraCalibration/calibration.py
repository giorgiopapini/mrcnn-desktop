import numpy as np
import cv2
import os
import glob
import time
import json

import constants
from App.UI.Common.SettingsDecoder import SettingsDecoder


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


class Calibrator:
    objpoints = []
    imgpoints = []
    images = []

    image_saving_state = False
    current_time = None

    def __init__(self, rows_num, cols_num):
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']
        self.SAVE_IMG_CHAR = SettingsDecoder['SAVE_IMG_CHAR']
        self.CALIBRATION_IMAGES_NEEDED = SettingsDecoder['CALIBRATION_IMAGES_NEEDED']

        self.rows = rows_num - 1
        self.cols = cols_num - 1

        self.objp = np.zeros((self.rows * self.cols, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.cols, 0:self.rows].T.reshape(-1, 2)

        self.load_images()

    def load_images(self):
        self.images = glob.glob('**App/CameraCalibration/images/calibrate*.jpg')

    def capture_images(self):
        cap = cv2.VideoCapture(0)
        if SettingsDecoder['ADDRESS'] is not '':
            cap.open(SettingsDecoder['ADDRESS'])  # registra i dati dalla webcam del telefono

        index = 0
        while True:
            success, real_img = cap.read()
            real_img = constants.Video.resize(real_img)

            img = real_img.copy()

            self.__manage_image_saving()
            self.__try_show_commands(img=img)
            self.__try_show_saved_message(img=img)

            cv2.imshow(constants.CALIBRATION_WINDOW_NAME, img)

            keys = cv2.waitKey(1) & 0xFF
            if keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
                cv2.destroyAllWindows()
                break
            if keys == ord(self.SAVE_IMG_CHAR) or keys == ord(self.SAVE_IMG_CHAR.upper()):
                if not self.image_saving_state:
                    if index < self.CALIBRATION_IMAGES_NEEDED:
                        self.__save_image(img=real_img, index=index)
                        index += 1
                    else:
                        cv2.destroyAllWindows()
                        break
            elif cv2.getWindowProperty(constants.CALIBRATION_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

    def __manage_image_saving(self):
        if self.image_saving_state:
            if time.time() - self.current_time > constants.SAVING_TIME:
                self.image_saving_state = False

    def __try_show_commands(self, img):
        if not self.image_saving_state:
            cv2.putText(
                img,
                f"Premi '{self.SAVE_IMG_CHAR}' per salvare l'immagine",
                (20, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )
            cv2.putText(
                img,
                f"Premi '{self.QUIT_CHAR}' per uscire",
                (20, 45),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (255, 0, 0),
                2
            )

    def __try_show_saved_message(self, img):
        if self.image_saving_state:
            cv2.putText(
                img,
                f"Salvataggio...",
                (20, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                .7,
                (0, 255, 0),
                2
            )

    def __save_image(self, img, index):
        path = f"{os.path.dirname(os.path.abspath(__file__))}/CameraCalibration/images"
        cv2.imwrite(f"{path}/calibrate_{index}.jpg", img)
        self.current_time = time.time()
        self.image_saving_state = True

    def calibrate(self):
        gray = None
        index = 0
        for image in self.images:
            img = cv2.imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            chessboard_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
            ret, corners = cv2.findChessboardCorners(gray, (self.cols, self.rows), chessboard_flags)

            if ret:
                self.objpoints.append(self.objp)
                self.imgpoints.append(corners)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

                cv2.drawChessboardCorners(img, (self.cols, self.rows), corners2, ret)
                cv2.imwrite(f"App/CameraCalibration/corners/chessboard_corners_{index}.jpg", img)
                cv2.waitKey(1500)
                index += 1

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.objpoints,
            self.imgpoints,
            gray.shape[::-1],
            None,
            None
        )
        self.__save_camera_data(ret, mtx, dist, rvecs, tvecs)

    def __save_camera_data(self, ret, mtx, dist, rvecs, tvecs):
        camera = {}

        for variable in ['ret', 'mtx', 'dist', 'rvecs', 'tvecs']:
            camera[variable] = eval(variable)

        with open(f"App/Camera/camera.json", 'w') as file:
            json.dump(camera, file, indent=4, cls=NumpyEncoder)
