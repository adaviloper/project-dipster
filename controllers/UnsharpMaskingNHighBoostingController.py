import cv2
import numpy as np
import sys

class UnsharpMaskingNHighBoostingController:

    def get_gaussian_low_pass_filter(self, params):

        image_path = 'controllers/assets/images/' + params['image']
        input_image = cv2.imread(image_path, 0)
        gaussian = cv2.GaussianBlur(input_image, params['windowSize'], 10.0)
        unsharp_image = cv2.addWeighted(input_image, 1.5, gaussian, -0.5, 0, input_image)

        return unsharp_image

    def unsharpMasking(self, image, params):

        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        smoothImg = self.get_gaussian_low_pass_filter(input_image)

        mask = np.subtract(input_image, smoothImg)

        result = input_image + 1 * mask
        # Should return [input_image, smoothImg, result]
        return result
