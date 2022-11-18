import glob
import json

import cv2
import numpy as np


class Camera:
    camera_matrix = None
    distortion_data = None
    undistorted_camera_matrix = None

    def __init__(self):
        self.load_camera_data_from_json()

    def load_camera_data_from_json(self):
        with open('camera.json', 'r') as file:
            camera_data = json.load(file)
            self.camera_matrix = np.array(camera_data['mtx'])
            self.distortion_data = np.array(camera_data['dist'])

    def try_calc_undistorted_camera_matrix(self):
        try:
            self.calc_undistorted_camera_matrix()
        except IndexError:
            print('[ERROR] => You need to take chessboard pictures first')

    def calc_undistorted_camera_matrix(self):
        images = glob.glob('CameraCalibration/images/calibrate*.jpg')
        frame = cv2.imread(images[0])
        height, width = frame.shape[:2]
        self.undistorted_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
            self.camera_matrix,
            self.distortion_data,
            (height, width),
            0,  # 1
            (height, width)
        )
