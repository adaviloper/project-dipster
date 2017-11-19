from __future__ import unicode_literals, print_function, generators, division
import numpy as np
import cv2
from scipy import signal
from view import View

# Call convolution or correlation function with an image as input

class ConvolutionCorrelationController:

    def zero_padding(self,org, mask):
        w, h = mask.shape
        print('org padding')

        if w is 1:
            x = (h - 1) / 2
            for i in range(int(x)):
                org = np.insert(org, 0, 0, axis=1)
                org = np.insert(org, org.shape[1], 0, axis=1)
        if h is 1:
            y = (w - 1) / 2
            for j in range(int(y)):
                org = np.insert(org, 0, 0, axis=0)
                org = np.insert(org, org.shape[0], 0, axis=0)

        x = (w + 1) / 2
        y = (h + 1) / 2

        if w is not 1 and h is not 1:
            for i in range(int(x)):
                org = np.insert(org, 0, 0, axis=1)
                org = np.insert(org, org.shape[1], 0, axis=1)
            for j in range(int(y)):
                org = np.insert(org, 0, 0, axis=0)
                org = np.insert(org, org.shape[0], 0, axis=0)

        print('after padding')

        return org

    def convolt(self, img, mask):
        print('convolt')

        mask = np.rot90(mask, 2)
        mw, mh = mask.shape
        img = self.zero_padding(img, mask)
        w, h = img.shape
        offset = int((mw-1)/2)
        temp = np.zeros([w, h], dtype=float)
        for i in range(w - offset - 1):
            for j in range(h - offset - 1):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = np.sum(np.multiply(subImg, mask))
        print("after convolution")
        return temp

    def correlate(self, img, mask):
        img = self.zero_padding(img, mask)
        w, h = img.shape
        mw, mh = mask.shape
        offset = int((mw - 1) / 2)
        temp = np.zeros([w, h], dtype=float)
        for i in range(w - offset - 1):
            for j in range(h - offset - 1):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = np.sum(np.multiply(subImg, mask))
        return temp

    def zero_cropping(self, org, mask):
        print('org cropping')

        w, h = mask.shape

        if w is 1:
            x = (h - 1) / 2 + 1
            for i in range(int(x)):
                org = np.delete(org, 0, 1)
                org = np.delete(org, org.shape[1] - 1, 1)
        if h is 1:
            y = (w - 1) / 2 + 1
            for j in range(int(y)):
                org = np.delete(org, 0, 0)
                org = np.delete(org, org.shape[0] - 1, 0)

        x = (w + 1) / 2 + 1
        y = (h + 1) / 2 + 1

        if w is not 1 and h is not 1:
            for i in range(int(x)):
                org = np.delete(org, 0, 1)
                org = np.delete(org, org.shape[1] - 1, 1)
            for j in range(int(y)):
                org = np.delete(org, 0, 0)
                org = np.delete(org, org.shape[0] - 1, 0)

        print('after cropping')

        return org

    def convolution(self, image, mask=None):
        # input: orginal image and mask
        # output: image after convolution
        if mask is None:
            mask = np.array([[1, 2, 1],
                      [2, 4, 2],
                      [1, 2, 1]], dtype=float
                     )/16

        image = self.convolt(image, mask)
        image = self.zero_cropping(image, mask)

        return image
        #return image.astype(np.uint8)

    def correlation(self, image, mask=None):
        # input: orginal image and mask
        # output: image after correlation

        if mask is None:
            mask = np.array([[1, 2, 1],
                      [2, 4, 2],
                      [1, 2, 1]], dtype=float
                     )/16

        image = self.convolt(image, mask)
        image = self.zero_cropping(image, mask)
        return image
        #return image.astype(np.uint8)

    def test(self):

        # for test
        img = cv2.imread("Lenna.png", 0)

        x = np.array([[1, 1, 1, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 1, 1, 1],
                      [0, 0, 1, 1, 0],
                      [0, 1, 1, 0, 0]],
                     )
        w = np.array([[1, 2, 1],
                      [2, 4, 2],
                      [1, 2, 1]], dtype=float
                     )
        w_1 = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]], dtype=float)

        y = signal.convolve2d(x, w/16, 'valid')

        # print(x)
        # print(self.convolution(x, w/16))
        # print(y)
        img = self.convolution(img, w/16)

        self.display_image("convolution",img)

    def display_image(self, window_name, image):
        """A function to display image"""
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
