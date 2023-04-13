import cv2
import constants
from App.UI.Common.SettingsDecoder import SettingsDecoder


class MaskChooser:
    def __init__(self, img, mrcnn_mask, grabcut_mask):
        self.img = img
        self.mrnn_mask = mrcnn_mask
        self.grabcut_mask = grabcut_mask
        self.active_mask = self.mrnn_mask
        self.CHANGE_MASK_CHAR = SettingsDecoder['CHANGE_MASK_CHAR']
        self.SELECT_MASK_CHAR = SettingsDecoder['SELECT_MASK_CHAR']

    def __write_mask(self, mask_image):
        contours, _ = cv2.findContours(self.active_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(mask_image, contours, -1, (0, 255, 0), 2)
        cv2.fillPoly(mask_image, contours, (0, 255, 255))

    def __get_translucent_effect_image(self, mask_image):
        alpha = 0.40
        return cv2.addWeighted(mask_image, alpha, self.img, 1 - alpha, 0)

    def __write_commands(self, mask_image):
        cv2.putText(
            mask_image,
            f"Premi '{self.CHANGE_MASK_CHAR}' cambiare mask",
            (20, 20),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

        cv2.putText(
            mask_image,
            f"Premi '{self.SELECT_MASK_CHAR}' per selezionare la mask e proseguire",
            (20, 45),
            cv2.FONT_HERSHEY_DUPLEX,
            .7,
            (255, 0, 0),
            2
        )

    def choose_mask(self):
        while True:
            mask_image = self.img.copy()
            self.__write_mask(mask_image)
            mask_image = self.__get_translucent_effect_image(mask_image)
            self.__write_commands(mask_image)
            cv2.imshow(constants.MASK_CHOOSER_WINDOW_NAME, mask_image)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(self.CHANGE_MASK_CHAR) or key == ord(self.CHANGE_MASK_CHAR.upper()):
                self.active_mask = self.grabcut_mask if self.active_mask is self.mrnn_mask else self.mrnn_mask
            elif key == ord(self.SELECT_MASK_CHAR) or key == ord(self.SELECT_MASK_CHAR.upper()):
                cv2.destroyAllWindows()
                return self.active_mask
