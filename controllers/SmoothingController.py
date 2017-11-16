import cv2
import numpy as np
from skimage.exposure import rescale_intensity
from view import View

# primary method to be called imagesmoothing. For example: smoothing_obj = imageSmoothing(image, windowSize)
class SmoothingController:
    image = None

    def smoothing(self, params):

        image_path = 'controllers/assets/images/' + params['image']

        # image_file = Path(image_path)
        # if image_file.is_file():
        #     print('file exists')
        # else:
        #     print(params['image'])
        #     print('file does not exist')
        input_image = cv2.imread(image_path, 0)
        image_output_path = 'controllers/assets/images/out/dog_out_Tyler_asdf.png'
        cv2.imwrite(image_output_path, input_image)
        view = View()
        output = view.render(message=[image_output_path])
        return '200 okay', output
