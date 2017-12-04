import cv2
import numpy as np
from skimage.exposure import rescale_intensity
from view import View
from controllers import SmoothingController

class UnsharpMaskingAndHighBoostingController:

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

        return output


    def unsharpMasking(self, params):
        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        """
        Do any necessary calculations below here
        """
        smooth_img = self.smoothing(params)

        mask = np.subtract(input_image, smooth_img)

        result = input_image + 1 * mask

        """
        Do any necessary calculations above here
        """
        # Leave these image paths as the path to the file names that the outputs should be saved to
        smooth_image_output_path = 'controllers/assets/images/out/smooth_' + params['image']
        result_image_output_path = 'controllers/assets/images/out/result_' + params['image']
        # Write your images to those files
        cv2.imwrite(smooth_image_output_path, smooth_img)
        cv2.imwrite(result_image_output_path, result)
        # Call in the view that the paths will be printed to
        view = View()
        # message is an array that lists all of the image paths
        # There is no need to pass the original image as that will always be displayed
        # Should return [input_image, smooth_img, result]
        output = view.render(message=[smooth_image_output_path, result_image_output_path])
        return '200 okay', output
