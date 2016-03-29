import cv2
import numpy
from os import system


class ImageTools(object):
    
    @staticmethod #TODO - move it to the right class!
    def copy_file_from_device(source_path,dist_path):
        cmd = "adb pull %s %s" %(source_path,dist_path)
        system(cmd)

    @staticmethod
    def find_sub_image_in_image(image,sub_image):
        result = cv2.matchTemplate(image,sub_image,cv2.TM_CCOEFF_NORMED)
        maximum = result.max()
        sub_image_location = numpy.unravel_index(result.argmax(),result.shape)
        stats = matchStats(maximum,sub_image_location)
        return stats

    @staticmethod
    def crop_image(image,crop_dict):
        cropped_image= image[crop_dict["y_min"]:crop_dict["y_max"], \
                             crop_dict["x_min"]:crop_dict["x_max"], \
                             crop_dict["z_min"]:crop_dict["z_max"] ]
        return cropped_image

class matchStats(object):
    def __init__(self,max_value,max_location):
        self.max_value = max_value
        self.max_location = max_location
        