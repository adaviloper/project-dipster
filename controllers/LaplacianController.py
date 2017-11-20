from __future__ import unicode_literals, print_function, generators, division

from controllers.ConvolutionCorrelationController import ConvolutionCorrelationController
from view import View
import cv2
import numpy as np


# Call LaplacianInitial function for Laplacian operation

class LaplacianController:
    def filter(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        image = cv2.imread(image_path, 0)
        lap = LaplacianController()
        output = lap.laplacian(image)

        image_output_path = 'controllers/assets/images/out/laplacian_' + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message = [image_output_path])
        return '200 okay', output

    def laplacian(self, img = None, mask = None):
        print("laplacian")
        if img is None:
            image_path = 'controllers/assets/images/'
            img = cv2.imread(image_path, 0)

        if mask is None:
            mask = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
        img = self.convolution(img, mask)
        img = self.post_process_image(img)
        return img

    def convolution(self, img, mask):
        print("convolution")
        conv = ConvolutionCorrelationController()
        img = conv.convolt(img, mask)
        img = conv.zero_cropping(img, mask)

        return img

    def post_process_image(self, image):

        maxIntensity = image.max()
        minIntensity = image.min()
        # print(maxIntensity)
        # print(minIntensity)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i, j] = (256 - 1) / (maxIntensity - minIntensity) * (image[i, j] - minIntensity)

        return image.astype(np.uint8)

    def test(self):
        print("test")
        x = np.array([[1, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1],
                      [0, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0]],
                     )
        img = self.laplacian()

        # for imag diaplay
        # self.display_image("laplace", img)

    def display_image(self, window_name, image):
        """A function to display image"""
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)