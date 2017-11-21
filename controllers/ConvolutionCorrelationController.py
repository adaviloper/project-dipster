from __future__ import unicode_literals, print_function, generators, division
import numpy as np
import cv2
from scipy import signal
from view import View

# Call ConvolutionInitial For Convolution operation
# Call CorrelationInitial For Correlation operation

class ConvolutionCorrelationController:

    def ConvolutionInitial(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        image = cv2.imread(image_path, 0)
        conv = ConvolutionCorrelationController()
        output = conv.convolution(image)

        image_output_path = 'controllers/assets/images/out/' + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message=[image_output_path])
        return '200 okay', output

    def CorrelationInitial(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        image = cv2.imread(image_path, 0)
        conv = ConvolutionCorrelationController()
        output = conv.correlation(image)

        image_output_path = 'controllers/assets/images/out/' + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message=[image_output_path])
        return '200 okay', output

    def convolution(self, image=None, mask=None):
        # input: orginal image and mask
        # output: image after convolution
        if image is None:
            image_path = 'controllers/assets/images/'
            image = cv2.imread(image_path, 0)

        if mask is None:
            np.array([[0, -1, 1]])

        image = self.convolt(image, mask)
        image = self.zero_cropping(image, mask)

        return image.astype(np.uint8)

    def correlation(self, image=None, mask=None):
        # input: orginal image and mask
        # output: image after correlation
        if image is None:
            image_path = 'controllers/assets/images/'
            image = cv2.imread(image_path, 0)

        if mask is None:
            mask = np.array([[0, -1, 1]])

        image = self.convolt(image, mask)
        image = self.zero_cropping(image, mask)

        return image.astype(np.uint8)

    def zero_padding(self,org, mask):
        w, h = mask.shape
        size = (max(w, h) - 1) / 2

        for i in range(int(size)):
            org = np.insert(org, 0, 0, axis=1)
            org = np.insert(org, org.shape[1], 0, axis=1)
            org = np.insert(org, 0, 0, axis=0)
            org = np.insert(org, org.shape[0], 0, axis=0)

        return org

    def convolt(self, img, mask):

        img = self.zero_padding(img, mask)

        w, h = img.shape
        mw, mh = mask.shape

        if mw < mh:
            size = int((mh - 1) / 2)
            for i in range(size):
                mask = np.insert(mask, 0, 0, axis=0)
                mask = np.insert(mask, mask.shape[0], 0, axis=0)
        elif mw > mh:
            size = int((mw - 1) / 2)
            for i in range(size):
                mask = np.insert(mask, 0, 0, axis=1)
                mask = np.insert(mask, mask.shape[1], 0, axis=1)
        mw, mh = mask.shape
        mask = np.rot90(mask, 2)

        offset = int((len(mask) - 1) / 2)

        temp = np.zeros([w, h], dtype=float)
        for i in range(w - offset - 1):
            for j in range(h - offset - 1):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = np.sum(np.multiply(subImg, mask))

        return temp

    def correlate(self, img, mask):
        img = self.zero_padding(img, mask)
        w, h = img.shape
        mw, mh = mask.shape

        if mw < mh:
            size = int((mh - 1) / 2)
            for i in range(size):
                mask = np.insert(mask, 0, 0, axis=0)
                mask = np.insert(mask, mask.shape[0], 0, axis=0)
        elif mw > mh:
            size = int((mw - 1) / 2)
            for i in range(size):
                mask = np.insert(mask, 0, 0, axis=1)
                mask = np.insert(mask, mask.shape[1], 0, axis=1)

        mw, mh = mask.shape

        offset = int((len(mask) - 1) / 2)

        temp = np.zeros([w, h], dtype=float)
        for i in range(w - offset - 1):
            for j in range(h - offset - 1):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = np.sum(np.multiply(subImg, mask))

        return temp

    def zero_cropping(self, org, mask):
        w, h = mask.shape
        size = (max(w, h) - 1) / 2
        print(size)
        for i in range(int(size)):
            org = np.delete(org, 0, 1)
            org = np.delete(org, org.shape[1] - 1, 1)

            org = np.delete(org, 0, 0)
            org = np.delete(org, org.shape[0] - 1, 0)

        return org



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