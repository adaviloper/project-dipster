import cv2
import numpy as np
from skimage.exposure import rescale_intensity
from view import View


# primary method to be called imagesmoothing. For example: smoothing_obj = imageSmoothing(image, windowSize)
class SmoothingController:
    image = None

    def smoothing(self, params):

        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        # gets Windowsize from params
        windowSize = params['windowSize']
        windowSize = int(windowSize[0])
        print("window size is ", windowSize)
        kernel = np.ones((windowSize, windowSize), dtype = "float")
        (iH, iW) = kernel.shape[:2]

        sum = 0
        for c in range(iH):
            for r in range(iW):
                sum = sum + kernel[c][r]

        kernel = kernel / sum

        # get dimentions of input image and kernel
        (iH, iW) = input_image.shape[:2]
        (kH, kW) = kernel.shape[:2]

        # Does zero padding
        pad = int((kW - 1) / 2)
        image = cv2.copyMakeBorder(input_image, pad, pad, pad, pad,
                                   cv2.BORDER_REPLICATE)
        output = np.zeros((iH, iW), dtype = "float32")

        # performs actual convolution by sliding kernal over image
        for y in np.arange(pad, iH + pad):
            for x in np.arange(pad, iW + pad):
                roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]

                k = (roi * kernel).sum()

                output[y - pad, x - pad] = k

        # rescale the output image to be in the range [0, 255]
        output = rescale_intensity(output, in_range = (0, 255))
        output = (output * 255).astype("uint8")

        # saves output and displays it on the page
        image_output_path = 'controllers/assets/images/out/' + str(windowSize) + 'x' + str(windowSize) + params['image']
        cv2.imwrite(image_output_path, output)
        view = View()
        output = view.render(message = [image_output_path])
        return '200 okay', output

    def convolve(self, image, kernel):
        # cv2.imshow("original image", image)
        # grab the spatial dimensions of the image, along with
        # the spatial dimensions of the kernel
        (iH, iW) = image.shape[:2]
        (kH, kW) = kernel.shape[:2]

        # noiseImage = np.zeros((iH,iW), np.uint8)
        # noiseImage = cv2.randn(noiseImage,(0), (255))
        # noiseImage = noiseImage + image
        # image = noiseImage
        #
        # cv2.imshow("noisyImage", noiseImage)

        # does zero padding on the image
        pad = int((kW - 1) / 2)
        image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
                                   cv2.BORDER_REPLICATE)
        output = np.zeros((iH, iW), dtype = "float32")

        # performs actual convolution by sliding kernal over image
        for y in np.arange(pad, iH + pad):
            for x in np.arange(pad, iW + pad):
                roi = image[y - pad:y + pad + 1, x - pad:x + pad + 1]

                k = (roi * kernel).sum()

                output[y - pad, x - pad] = k

        # rescale the output image to be in the range [0, 255]
        output = rescale_intensity(output, in_range = (0, 255))
        output = (output * 255).astype("uint8")

        # cv2.imshow("output", output)
        # cv2.waitKey(0)
        # return the output image
        return output
