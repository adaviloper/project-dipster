import numpy as np
import cv2
# from __future__ import unicode_literals, print_function, generators, division
from scipy import signal
from view import View


# Call ConvolutionInitial For Convolution operation
# Call CorrelationInitial For Correlation operation

class ConvolutionCorrelationController:
    def ConvolutionInitial(self, params):
        #print('hit')
        image_path = 'controllers/assets/images/' + params['image']
        image = cv2.imread(image_path, 0)
        conv = ConvolutionCorrelationController()
        s = (5, 5)
        mask = np.ones(s)
        #mask = np.array([[1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1]], dtype=float)

        output = conv.convolution(image, mask/(len(mask)**2))
        output = output.astype(np.uint8)
        #output = conv.post_process_image(output)

        image_output_path = 'controllers/assets/images/out/convolution_' + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message=[image_output_path])
        return '200 okay', output

    def CorrelationInitial(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        image = cv2.imread(image_path, 0)
        corr = ConvolutionCorrelationController()
        output = corr.correlation(image)
        output = output.astype(np.uint8)

        image_output_path = 'controllers/assets/images/out/correlation_' + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message=[image_output_path])
        return '200 okay', output

    def convolution(self, image, mask=None):
        # input: orginal image and mask
        # output: image after convolution
        # if image is None:
        #     image_path = 'controllers/assets/images/'
        #     image = cv2.imread(image_path, 0)
        #
        if mask is None:
            mask = np.array([[0, -1, 1]])
        print("start convolution")

        conv = ConvolutionCorrelationController()
        image = conv.convolt(image, mask)
        print("convolution done")
        return image
        # return image.astype(np.uint8)

    def correlation(self, image, mask=None):
        # input: orginal image and mask
        # output: image after correlation
        # if image is None:
        #     image_path = 'controllers/assets/images/'
        #     image = cv2.imread(image_path, 0)
        #

        if mask is None:
            mask = np.array([[0], [1], [-1]])

        print("correlation", mask.shape)
        corr = ConvolutionCorrelationController()
        image = corr.correlate(image, mask)


        return image

    def zero_padding(self, org, size):
        w, h = org.shape
        print("zero padding")
        print("img shape before zero padding", w, h)


        m = int(w + 2 * size)
        n = int(h + 2 * size)
        temp = np.zeros((m, n), dtype=int)

        for i in range(size, w + size):
            for j in range(size, h + size):
                temp[i, j] = org[i - size, j - size]

        print('img shape after padding')
        print(temp.shape)
        return temp

    def mask_rotate(self, mask):
        w, h = mask.shape
        temp = np.zeros([w, h])
        for i in range(w):
            for j in range(h):
                temp[i, j] = mask[w - i - 1, h - j - 1]

        return temp

    def convolt(self, img, mask):
        #print("convolt")
        w, h = img.shape
        #print(w, h)
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



        size = (mw - 1) / 2

        img = self.zero_padding(img, int(size))
        mask = self.mask_rotate(mask)
        print("mask shape", mask.shape)
        print("print mask")
        print(mask)

        w, h = img.shape

        offset = int((len(mask) - 1) / 2)

        temp = np.zeros([w, h], dtype=float)
        for i in range(w - offset - int(mw/2)):
            for j in range(h - offset - int(mh/2)):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = int(np.sum(np.multiply(subImg, mask)))

        image = self.zero_cropping(temp, int(size))

        return image

    def correlate(self, img, mask):

        w, h = img.shape
        mw, mh = mask.shape
        print("correlate", mask)
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
        size = (mw - 1) / 2
        print("before padding", mask)
        img = self.zero_padding(img, int(size))

        offset = int((len(mask) - 1) / 2)

        temp = np.zeros([w, h])
        for i in range(w - offset - int(mw/2)):
            for j in range(h - offset - int(mh/2)):
                subImg = img[i:i + mw, j:j + mh]

                temp[i + offset, j + offset] = int(np.sum(np.multiply(subImg, mask)))


        image = self.zero_cropping(temp, int(size))

        return image

    def zero_cropping(self, org, size):
        w, h = org.shape

        print('zero cropping')
        print("img shape before zero cropping", w, h)
        #print(type(size))
        m = w - 2 * size
        n = h - 2 * size
        #print(m, n)

        temp = np.zeros([int(m), int(n)])
        #print(temp.shape)

        for i in range(0, m):
            for j in range(0, n):
                temp[i, j] = org[i + size, j + size]
        print("img after cropping")
        print(temp.shape)
        return temp

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

        y = signal.convolve2d(x, w / 16, 'valid')

        # print(x)
        # print(self.convolution(x, w/16))
        # print(y)
        img = self.convolution(img, w / 16)

        self.display_image("convolution", img)

    def display_image(self, window_name, image):
        """A function to display image"""
        cv2.namedWindow(window_name)
        cv2.imshow(window_name, image)
        cv2.waitKey(0)

    def post_process_image(self, image):

        maxIntensity = image.max()
        minIntensity = image.min()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i, j] = (256 - 1) / (maxIntensity - minIntensity) * (image[i, j] - minIntensity)

        return image.astype(np.uint8)
