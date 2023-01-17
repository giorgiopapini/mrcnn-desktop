import cv2
import numpy as np


class MaskRefiner:

    @staticmethod
    def get_refined_mask_with_grabcut(img, mask):

        mask[mask > 0] = cv2.GC_PR_FGD
        mask[mask == 0] = cv2.GC_BGD

        fg_model = np.zeros((1, 65), dtype="float")
        bg_model = np.zeros((1, 65), dtype="float")
        (gcMask, bg_model, fg_model) = cv2.grabCut(
            img,
            mask,
            None,
            bg_model,
            fg_model,
            5,
            cv2.GC_INIT_WITH_MASK
        )

        output_mask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
        output_mask = (output_mask * 255).astype("uint8")

        return output_mask
