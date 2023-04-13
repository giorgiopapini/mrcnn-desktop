import cv2
import constants
from App.UI.Common.SettingsDecoder import SettingsDecoder


class MaskDrawer:

    def __init__(self, img, mask, inital_zoom_level=1, initial_zoom_factor=1.1):
        self.ZOOM_IN_CHAR = SettingsDecoder['ZOOM_IN_CHAR']
        self.ZOOM_OUT_CHAR = SettingsDecoder['ZOOM_OUT_CHAR']
        self.UP_CHAR = SettingsDecoder['UP_CHAR']
        self.DOWN_CHAR = SettingsDecoder['DOWN_CHAR']
        self.LEFT_CAR = SettingsDecoder['LEFT_CHAR']
        self.RIGHT_CHAR = SettingsDecoder['RIGHT_CHAR']
        self.QUIT_CHAR = SettingsDecoder['QUIT_CHAR']
        self.SHOW_MASK_CHAR = SettingsDecoder['SHOW_MASK_CHAR']

        self.original = img
        self.img = self.original.copy()
        self.mask = mask
        self.img_area = None
        self.zoom_level = inital_zoom_level
        self.zoom_factor = initial_zoom_factor

        self.move_x = 0
        self.move_y = 0

        self.blocked_right = False
        self.blocked_left = False
        self.blocked_up = False
        self.blocked_down = False

        self.drawing = False
        self.mode = True
        self.frame_x = 0
        self.frame_y = 0
        self.current_former_x = 0
        self.current_former_y = 0
        self.writing_bg = True

        self.show_mask = True

    def __manage_image_constraints(self, x, y, frame_width, frame_height, resized_image):
        if x + frame_width > resized_image.shape[1]:
            self.blocked_right = True
        elif y + frame_height > resized_image.shape[0]:
            self.blocked_down = True
        elif x + frame_width < self.img.shape[1]:
            self.blocked_left = True
        elif y + frame_height < self.img.shape[0]:
            self.blocked_up = True
        else:
            self.blocked_right = False
            self.blocked_left = False
            self.blocked_down = False
            self.blocked_up = False

    def __try_show_img(self, frame, base_img):
        try:
            if self.show_mask:
                alpha = 0.40
                result = cv2.addWeighted(frame, alpha, base_img, 1 - alpha, 0)
                cv2.imshow(constants.MASK_DRAWER_WINDOW_NAME, result)
                cv2.setMouseCallback(constants.MASK_DRAWER_WINDOW_NAME, self.draw_mask)
            else:
                cv2.imshow(constants.MASK_DRAWER_WINDOW_NAME, base_img)
        except cv2.error:
            pass

    def __navigate_image(self, key):
        if key == ord(self.ZOOM_IN_CHAR):
            self.zoom_level *= self.zoom_factor
        elif key == ord(self.ZOOM_OUT_CHAR):
            self.zoom_level /= self.zoom_factor
        elif key == ord(self.RIGHT_CHAR):
            if not self.blocked_right:
                self.move_x += 10
        elif key == ord(self.LEFT_CAR):
            if not self.blocked_left:
                self.move_x -= 10
        elif key == ord(self.UP_CHAR):
            if not self.blocked_up:
                self.move_y -= 10
        elif key == ord(self.DOWN_CHAR):
            if not self.blocked_down:
                self.move_y += 10

    def draw_mask(self, event, former_x, former_y, flags, param):
        former_x = int((self.frame_x + former_x) / (self.zoom_level * self.zoom_factor))
        former_y = int((self.frame_y + former_y) / (self.zoom_level * self.zoom_factor))
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.writing_bg = False
            self.current_former_x, self.current_former_y = former_x, former_y

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

        if event == cv2.EVENT_RBUTTONDOWN:
            self.drawing = True
            self.writing_bg = True
            self.current_former_x, self.current_former_y = former_x, former_y

        elif event == cv2.EVENT_RBUTTONUP:
            self.drawing = False

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                if self.mode:
                    if self.writing_bg:
                        cv2.line(self.mask, (self.current_former_x, self.current_former_y), (former_x, former_y), (0, 0, 0), 3)
                    else:
                        cv2.line(self.mask, (self.current_former_x, self.current_former_y), (former_x, former_y), (255, 255, 255),3)
                    self.current_former_x = former_x
                    self.current_former_y = former_y

        return former_x, former_y

    def __load_img(self, original_img):
        new_image = original_img.copy()
        contours, _ = cv2.findContours(self.mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(new_image, contours, -1, (0, 255, 0), 2)
        cv2.fillPoly(new_image, contours, (0, 255, 255))
        return new_image

    def get_final_mask(self):
        frame_width = self.img.shape[1]
        frame_height = self.img.shape[0]

        while True:
            img_with_mask = self.__load_img(self.original)
            resized_image = cv2.resize(
                img_with_mask,
                None,
                fx=self.zoom_level * self.zoom_factor,
                fy=self.zoom_level * self.zoom_factor,
                interpolation=cv2.INTER_LINEAR
            )
            base_img = cv2.resize(
                self.img,
                None,
                fx=self.zoom_level * self.zoom_factor,
                fy=self.zoom_level * self.zoom_factor,
                interpolation=cv2.INTER_LINEAR
            )

            x = int((resized_image.shape[1] - frame_width) / 2) + self.move_x
            y = int((resized_image.shape[0] - frame_height) / 2) + self.move_y
            self.frame_x = x
            self.frame_y = y

            self.__manage_image_constraints(x, y, frame_width, frame_height, resized_image)

            frame = resized_image[y:y + frame_height, x:x + frame_width]
            base_img = base_img[y:y + frame_height, x:x + frame_width]
            self.__try_show_img(frame, base_img)

            key = cv2.waitKey(1) & 0xFF
            self.__navigate_image(key)
            if key == ord(self.SHOW_MASK_CHAR):
                self.show_mask = True if self.show_mask is False else False
            elif key == ord(self.QUIT_CHAR) or key == 27:
                cv2.destroyAllWindows()
                return self.mask
