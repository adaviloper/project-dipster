import cv2
import numpy as np
from controllers import ConvolutionCorrelationController
from view import View


class FirstOrderDerivativeController:

    def smoothing(self, params):

        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        # gets Windowsize from params
        windowSize = params['windowSize']
        windowSize = int(windowSize[0])

        print("window size is ", windowSize)

        kernel = np.ones((windowSize, windowSize), dtype="float")
        (iH, iW) = kernel.shape[:2]

        sum = 0
        for c in range(iH):
            for r in range(iW):
                sum = sum + kernel[c][r]

        kernel = kernel / sum

        smooth_img = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, input_image, kernel)

        return smooth_img


    def post_process_image(self, image):

        maxIntensity = image.max()
        minIntensity = image.min()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                image[i, j] = (256 - 1) / (maxIntensity - minIntensity) * (image[i, j] - minIntensity)

        return image.astype(np.uint8)


    def sharpening(self, params):
        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        windowSize = 3
        print("windowSize:", windowSize)

        smooth_img = self.smoothing(params)

        filterOperator = params['filterOperator']

        if filterOperator == "sobel":
            # print("sobel filter")

            if windowSize == 3:
                sobelx = np.matrix([[1, 0, -1],
                                    [2, 0, -2],
                                    [1, 0, -1]])

                sobely = np.matrix([[1, 2, 1],
                                     [0, 0, 0],
                                     [-1, -2, -1]])

                (kH, kW) = (3, 3)

            kernelx = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, smooth_img, sobelx)
            kernely = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, smooth_img, sobely)

            kernelx = self.post_process_image(kernelx)
            kernely = self.post_process_image(kernely)

        elif filterOperator == "prewitt":
            # print("prewitt fiter")

            if windowSize == 3:
                prewittx = np.matrix([[-1, 0, 1],
                                    [-1, 0, 1],
                                    [-1, 0, 1]])

                prewitty = np.matrix([[-1, -1, -1],
                                     [0, 0, 0],
                                     [1, 1, 1]])

                (kH, kW) = (3, 3)

            kernelx = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, smooth_img, prewittx)
            kernely = ConvolutionCorrelationController.convolution(ConvolutionCorrelationController, smooth_img, prewitty)

            kernelx = self.post_process_image(kernelx)
            kernely = self.post_process_image(kernely)

        #Computing the Gradient Magnitude
        gradMag = np.zeros(kernelx.shape)

        for i in range(kernelx.shape[0]):
            for j in range(kernelx.shape[1]):
                I1 = kernelx[i][j]
                I2 = kernely[i][j]

                gradMag[i][j] = np.sqrt(np.add(I1 ** 2, I2 ** 2))

        gradMag = self.post_process_image(gradMag)


        # Computing the image sharpening
        sharp_img = smooth_img + gradMag
        sharp_img = self.post_process_image(smooth_img)

        smooth_output_path = 'controllers/assets/images/out/smooth_' + params['image']
        gradMag_output_path = 'controllers/assets/images/out/gradMag_' + params['image']
        sharp_output_path = 'controllers/assets/images/out/sharp_' + params['image']

        cv2.imwrite(smooth_output_path, smooth_img.astype("uint8"))
        cv2.imwrite(gradMag_output_path, gradMag)
        cv2.imwrite(sharp_output_path, sharp_img)

        view = View()
        output = view.render(message = [smooth_output_path + '?Title=Smoothed_Image', gradMag_output_path + '?Title=Gradient_Magnitude_Image', sharp_output_path + '?Title=Sharped_Image'])
        return '200 okay', output
