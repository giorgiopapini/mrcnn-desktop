import cv2
from keras.models import load_model

from App.ShapeDetection.MaskRefiner.mask_refiner import MaskRefiner
from App.ShapeDetection.mrcnn.models.deeplab import Deeplabv3, relu6, BilinearUpsampling, DepthwiseConv2D
from App.ShapeDetection.mrcnn.utils.learning.metrics import dice_coef, precision, recall
from App.ShapeDetection.mrcnn.utils.io.data import save_results, load_test_images, DataGen

import constants


class MRCNNExecutor:
    COLOR_SPACE = 'rgb'
    PATH = './App/ShapeDetection/mrcnn/data/Medetec_foot_ulcer_224/'
    MODEL_FILENAME = '2019-12-19 01%3A53%3A15.480800.hdf5'
    SAVE_PATH = '2019-12-19 01%3A53%3A15.480800/'

    def __init__(self, img):
        self.img = img
        self.__save_original_img()

    def __save_original_img(self):
        full_path = f"{self.PATH}test/images/original.png"
        cv2.imwrite(full_path, self.img)

    def generate_and_save_mask(self):
        data_gen = DataGen(self.PATH, split_ratio=0.0, x=constants.MRCNN_SIZE, y=constants.MRCNN_SIZE, color_space=self.COLOR_SPACE)
        x_test, test_label_filenames_list = load_test_images(self.PATH)

        model = Deeplabv3(input_shape=(constants.MRCNN_SIZE, constants.MRCNN_SIZE, 3), classes=1)
        model = load_model('./App/ShapeDetection/mrcnn/training_history/' + self.MODEL_FILENAME
                           , custom_objects={'recall': recall,
                                             'precision': precision,
                                             'dice_coef': dice_coef,
                                             'relu6': relu6,
                                             'DepthwiseConv2D': DepthwiseConv2D,
                                             'BilinearUpsampling': BilinearUpsampling})

        for image_batch, label_batch in data_gen.generate_data(batch_size=len(x_test), test=True):
            prediction = model.predict(image_batch, verbose=1)
            save_results(prediction, 'rgb', self.PATH + 'test/predictions/' + self.SAVE_PATH, test_label_filenames_list)
            self.refine_mask_with_grabcut()
            break

    def refine_mask_with_grabcut(self):
        refined_mask = MaskRefiner.get_refined_mask_with_grabcut(
            img=self.img,
            mask=self.get_saved_mask()
        )
        cv2.imwrite(f"{self.PATH}test/predictions/2019-12-19 01%3A53%3A15.480800/original.png", refined_mask)

    def get_saved_mask(self):
        mask = cv2.imread(f"{self.PATH}test/predictions/2019-12-19 01%3A53%3A15.480800/original.png").astype('uint8') * 255
        return cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
