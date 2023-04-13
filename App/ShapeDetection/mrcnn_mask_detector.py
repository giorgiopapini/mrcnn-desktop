import multiprocessing
from tkinter import *

import constants
import cv2

from App.ShapeDetection.MaskChooser.mask_chooser import MaskChooser
from App.ShapeDetection.MaskDrawer.mask_drawer import MaskDrawer
from App.ShapeDetection.MaskRefiner.mask_refiner import MaskRefiner
from App.ShapeDetection.manual_shape_detector import ManualShapeDetector
from App.ShapeDetection.mrcnn.mrcnn_executor import MRCNNExecutor


class MRCNNShapeDetector(ManualShapeDetector):
    def __init__(self, input_type=constants.DetectionInputType.VIDEO, img_path=""):
        super().__init__(input_type, img_path)

    def __execute_mask_rcnn(self):
        resized_img = self.__get_resized_img_to_mrcnn_required_size()
        mrcnn_executor = MRCNNExecutor(img=resized_img)
        self.__create_and_run_mrcnn_process(mrcnn_executor=mrcnn_executor)

        raw_mask = mrcnn_executor.get_saved_mask()
        del mrcnn_executor

        raw_grabcut = MaskRefiner.get_refined_mask_with_grabcut(
            resized_img,
            raw_mask
        )

        grabcut_mask = self.__get_resized_mask_to_original_size(raw_grabcut)
        mask = self.__get_resized_mask_to_original_size(raw_mask)
        return mask, grabcut_mask

    def __create_and_run_mrcnn_process(self, mrcnn_executor):
        mrcnn_process = multiprocessing.Process(target=mrcnn_executor.generate_and_save_mask)
        mrcnn_process.start()
        mrcnn_process.join()

    def __get_resized_mask_to_original_size(self, mask):
        height = self.img.shape[0]
        width = self.img.shape[1]
        size = height if height > width else width
        return cv2.resize(mask, (size, size))

    def __get_resized_img_to_mrcnn_required_size(self):
        height = self.img.shape[0]
        width = self.img.shape[1]
        new_img = None
        if height > width:
            delta = height - width
            new_img = cv2.copyMakeBorder(self.img, 0, 0, 0, delta, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        else:
            delta = width - height
            new_img = cv2.copyMakeBorder(self.img, 0, delta, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        return cv2.resize(new_img, (constants.MRCNN_SIZE, constants.MRCNN_SIZE))

    def try_start(self):
        try:
            status = self.start()
            return status
        except:
            return False

    def start(self):
        self.capture_img()
        if self.img is None:
            cv2.destroyAllWindows()
            return False
        else:
            mrcnn, grabcut = self.__execute_mask_rcnn()
            mask_chooser = MaskChooser(self.img, mrcnn, grabcut)
            self.mask = mask_chooser.choose_mask()
            mask_drawer = MaskDrawer(self.img, self.mask)
            self.mask = mask_drawer.get_final_mask()
            while True:
                self.img_contour = self.img.copy()
                self.write_commands()
                self.get_contours(save_shapes=False)
                cv2.imshow(constants.SHAPE_DETECTION_WINDOW_NAME, self.img_contour)

                key = self.get_pressed_key()
                if key == self.SCAN_CHAR:
                    self.get_contours(save_shapes=True)
                    cv2.destroyAllWindows()
                    return True
                elif key == self.QUIT_CHAR:
                    cv2.destroyAllWindows()
                    return False
                elif cv2.getWindowProperty(constants.SHAPE_DETECTION_WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                    return False
