# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv
import cv2

import numpy as np
from pathlib import Path

from view import View


class FilteringController:
    image = None
    filter = None
    filter_name = None
    cutoff = None
    order = None

    # def __init__(self, image, filter_name, cutoff, order = 0):
    #     """initializes the variables frequency filtering on an input image
    #     takes as input:
    #     image: the input image
    #     filter_name: the name of the mask to use
    #     cutoff: the cutoff frequency of the filter
    #     order: the order of the filter (only for butterworth
    #     returns"""
    #     self.image = image
    #     self.filter_name = filter_name
    #     if filter_name == 'ideal_l':
    #         self.filter = self.get_ideal_low_pass_filter
    #     elif filter_name == 'ideal_h':
    #         self.filter = self.get_ideal_high_pass_filter
    #     elif filter_name == 'butterworth_l':
    #         self.filter = self.get_butterworth_low_pass_filter
    #     elif filter_name == 'butterworth_h':
    #         self.filter = self.get_butterworth_high_pass_filter
    #     elif filter_name == 'gaussian_l':
    #         self.filter = self.get_gaussian_low_pass_filter
    #     elif filter_name == 'gaussian_h':
    #         self.filter = self.get_gaussian_high_pass_filter
    #
    #     self.cutoff = cutoff
    #     self.order = order

    def get_ideal_low_pass_filter(self, shape):
        """Computes a Ideal low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal low pass mask"""
        (rows, cols) = shape
        output = np.zeros(shape)
        for row in range(rows):
            for col in range(cols):
                distance = self.get_distance(col, cols, row, rows)
                if distance <= self.cutoff:
                    output[row, col] = 1
                else:
                    output[row, col] = 0
        return output

    def get_ideal_high_pass_filter(self, shape):
        """Computes a Ideal high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the ideal filter
        returns a ideal high pass mask

        #Hint: May be one can use the low pass filter function to get a high pass mask"""
        return 1.0 - self.get_ideal_low_pass_filter(shape)

    @staticmethod
    def get_distance(col, cols, row, rows):
        return ((row - rows / 2) ** 2 + (col - cols / 2) ** 2) ** 2

    def get_butterworth_low_pass_filter(self, shape, pxd = 1):
        """Computes a butterworth low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth low pass mask"""
        (rows, cols) = shape
        output = np.zeros(shape)
        for row in range(rows):
            for col in range(cols):
                distance = self.get_distance(col, cols, row, rows)
                denominator = 1 + (distance / self.cutoff) ** (2 * self.order)
                output[row, col] = 1 / denominator
        return output

    def get_butterworth_high_pass_filter(self, shape):
        """Computes a butterworth high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the butterworth filter
        order: the order of the butterworth filter
        returns a butterworth high pass mask

        #Hint: May be one can use the low pass filter function to get a high pass mask"""
        return 1.0 - self.get_butterworth_low_pass_filter(shape)

    def get_gaussian_low_pass_filter(self, shape):
        """Computes a gaussian low pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian low pass mask"""
        (rows, cols) = shape
        output = np.zeros(shape)
        for row in range(rows):
            for col in range(cols):
                distance = self.get_distance(col, cols, row, rows)
                output[row, col] = (pow(np.e, -(distance**2 / (2 * self.cutoff ** 2)))).real
        return output

    def get_gaussian_high_pass_filter(self, shape):
        """Computes a gaussian high pass mask
        takes as input:
        shape: the shape of the mask to be generated
        cutoff: the cutoff frequency of the gaussian filter (sigma)
        returns a gaussian high pass mask

        #Hint: May be one can use the low pass filter function to get a high pass mask"""
        return 1.0 - self.get_gaussian_low_pass_filter(shape)

    def post_process_image(self, image):
        """Post process the image to create a full contrast stretch of the image
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        1. Full contrast stretch (fsimage)
        2. take negative (255 - fsimage)
        """
        (rows, cols) = image.shape
        min_num = image[0, 0]
        max_num = image[0, 0]
        for row in range(rows):
            for col in range(cols):
                if image[row, col] > max_num:
                    max_num = image[row, col]
                if image[row, col] < min_num:
                    min_num = image[row, col]
        print(max_num, min_num)
        output = np.zeros(image.shape)
        for row in range(rows):
            for col in range(cols):
                output[row, col] = np.round((255/(max_num - min_num)) * (image[row, col] - min_num) + 0.5)
        return output

    def filtering(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        # image_file = Path(image_path)
        # if image_file.is_file():
        #     print('file exists')
        # else:
        #     print(params['image'])
        #     print('file does not exist')
        input_image = cv2.imread(image_path, 0)
        image_output_path = 'controllers/assets/images/out/dog_out.png'
        cv2.imwrite(image_output_path, input_image)
        view = View()
        output = view.render(message=[image_output_path,image_output_path])
        return '200 okay', output
        # return [dft_image, filtered_image, contrast_stretch_image]
