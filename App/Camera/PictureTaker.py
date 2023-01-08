import cv2

import constants
from App.Camera.camera_object import Camera
from App.UI.Common.SettingsDecoder import SettingsDecoder


class PictureTaker:
    def __init__(self):
        self.SCAN_CHAR = SettingsDecoder['SCAN_CHAR']
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']

        self.real_img = None

        self.camera = Camera()
        self.camera.try_calc_undistorted_camera_matrix()

        self.cap = constants.Video.initialize_capture("", SettingsDecoder['ADDRESS'])

    def take_picture(self):
        while True:
            self.real_img = constants.Video.read(
                self.cap,
                self.camera.camera_matrix,
                self.camera.distortion_data,
                self.camera.undistorted_camera_matrix
            )

            command_img = self.real_img.copy()
            self.__show_commands(command_img)
            cv2.imshow(constants.PICTURE_TAKER_WINDOW_NAME, command_img)

            key = self.get_pressed_key()
            if key == self.QUIT_CHAR:
                cv2.destroyAllWindows()
                return None
            elif key == self.SCAN_CHAR:
                cv2.destroyAllWindows()
                return self.real_img

    def __show_commands(self, command_img):
        cv2.putText(
            command_img,
            f"Premi '{self.SCAN_CHAR}' per scattare la foto",
            (20, 20),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            command_img,
            f"Premi '{self.QUIT_CHAR}' per uscire",
            (20, 45),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

    def get_pressed_key(self):
        keys = cv2.waitKey(1) & 0xFF

        if keys == ord(self.QUIT_CHAR) or keys == ord(self.QUIT_CHAR.upper()):
            return self.QUIT_CHAR
        elif keys == ord(self.SCAN_CHAR) or keys == ord(self.SCAN_CHAR.upper()):
            return self.SCAN_CHAR
