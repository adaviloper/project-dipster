import cv2
import numpy as np
# from skimage.exposure import rescale_intensity
from controllers import ConvolutionCorrelationController
from view import View

class UnsharpMaskingAndHighBoostingController:

    def smoothing(self, params):

        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        # gets Windowsize from params
        windowSize = params['windowSize']
        windowSize = int(windowSize[0])

        # gets Boosting rate
        boost = params['highBoostFilterType']

        #Get FilterType
        filterType = params['unsharpFilterType']
        if filterType == 'average':
            print("window size is ", windowSize)

            kernel = np.ones((windowSize, windowSize), dtype="float")
            (iH, iW) = kernel.shape[:2]

            sum = 0
            for c in range(iH):
                for r in range(iW):
                    sum = sum + kernel[c][r]

            kernel = kernel / sum

        elif filterType == 'gaussian':
            # print('Gaussian')

            windowSize = params['windowSize']
            windowSize = int(windowSize[0])
            print("window size is ", windowSize)

            if windowSize == 3:
                kernel = np.matrix([[1, 2, 1],
                                    [2, 4, 2],
                                    [1, 2, 1]])
                kernel = kernel / 16

                (kH, kW) = (3, 3)

            elif windowSize == 5:
                kernel = np.matrix([[1, 4, 6, 4, 1],
                                    [4, 16, 24, 16, 4],
                                    [6, 24, 36, 24, 6],
                                    [4, 16, 24, 16, 4],
                                    [1, 4, 6, 4, 1]])
                kernel = kernel / 256
                (kH, kW) = (5, 5)
            else:
                print('Choose a kernel size with either 3 or 5')


        smooth_img = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, input_image, kernel)

        # # rescale the output image to be in the range [0, 255]
        # output = rescale_intensity(smooth_img, in_range = (0, 255))
        # output = (output * 255).astype("uint8")

        return smooth_img

    def post_process_image(self, image):

        maxIntensity = image.max()
        minIntensity = image.min()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i, j] = (256 - 1) / (maxIntensity - minIntensity) * (image[i, j] - minIntensity)

        return image.astype(np.uint8)

    def unsharpMasking(self, params):
        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        boost = params['highBoostFilterType']

        #Compute image smoothing
        smooth_img = self.smoothing(params)

        #Generate the mask
        mask = np.subtract(input_image, smooth_img)

        #Boost the image with the appropriate value
        result = input_image + boost * mask

        result = self.post_process_image(result)

        # Leave these image paths as the path to the file names that the outputs should be saved to
        smooth_image_output_path = 'controllers/assets/images/out/smooth_' + params['image']
        result_image_output_path = 'controllers/assets/images/out/result_' + params['image']

        # Write the images to the controller path
        cv2.imwrite(smooth_image_output_path, smooth_img.astype("uint8"))
        cv2.imwrite(result_image_output_path, result)

        # Call in the view that the paths will be printed to
        view = View()
        output = view.render(message=[smooth_image_output_path + '?Title=Smoothed_Image', result_image_output_path + '?Title=HighBoosted_Image'])
        return '200 okay', output
