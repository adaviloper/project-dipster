import cv2
import numpy as np
import sys

from view import View


class UnsharpMaskingAndHighBoostingController:
    def get_gaussian_low_pass_filter(self, params):
        image_path = 'controllers/assets/images/' + params['image']
        input_image = cv2.imread(image_path, 0)
        gaussian = cv2.GaussianBlur(input_image, params['windowSize'], 10.0)
        unsharp_image = cv2.addWeighted(input_image, 1.5, gaussian, -0.5, 0, input_image)

        return unsharp_image

    def unsharpMasking(self, params):
        image_path = 'controllers/assets/images/' + params['image']

        input_image = cv2.imread(image_path, 0)

        unsharper = UnsharpMaskingAndHighBoostingController()
        """
        Do any necessary calculations below here
        """
        smooth_img = unsharper.get_gaussian_low_pass_filter(params)

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
