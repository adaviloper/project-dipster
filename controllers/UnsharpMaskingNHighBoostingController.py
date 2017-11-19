import cv2
import numpy as np
from skimage.exposure import rescale_intensity
from view import View
import sys
fc = sys.path.append('controllers/FilteringController')
from controllers import FilteringController

class UnsharpMaskingNHighBoostingController:
    image = None


    def get_gaussian_low_pass_filter(self, shape):

        (rows, cols) = shape
        output = np.zeros(shape)
        for row in range(rows):
            for col in range(cols):
                distance = self.get_distance(col, cols, row, rows)
                output[row, col] = (pow(np.e, -(distance**2 / (2 * self.cutoff ** 2)))).real
        return output

    def unsharpMasking(self, image, params):

        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        smoothImg = self.get_gaussian_low_pass_filter(input_image)
        return 0