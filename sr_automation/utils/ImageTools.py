import time
import slash
import cv2
import numpy
import Image
import pytesseract
from os import system
from sr_automation.utils.TakeSnapshot import TakeSnapshot
from logbook import Logger
log = Logger("ImageTools")


class ImageTools(object):
    SNAPSHOT_PATH = "/tmp/"
    CHROOT_PATH = "/data/sunriver/fs/limited/"
    DIST_PATH = "/tmp/"
    
    @staticmethod
    def find_sub_image_in_image(image_name,subImage_path,crop_boundries=None):
        snapshot = TakeSnapshot(slash.g.sunriver.linux.shell)
        snapshot.take_snapshot(ImageTools.SNAPSHOT_PATH, image_name)
        ImageTools.copy_file_from_device(ImageTools.CHROOT_PATH+ImageTools.SNAPSHOT_PATH+image_name, ImageTools.DIST_PATH)
        time.sleep(2)
        image = cv2.imread(ImageTools.DIST_PATH + image_name)
        if crop_boundries is not None:
            image = ImageTools.crop_image(image, crop_boundries)
        sub_image = cv2.imread(subImage_path)
        stats = ImageTools.find_max_match_sub_image_in_image(image, sub_image)
        log.info("best match percentage %f location (%f,%f)"% (stats.max_value,stats.max_location[0],stats.max_location[1]))
        log.info("image dimensions (%f,%f,%f)"%(image.shape[0],image.shape[1],image.shape[2]))
        return stats
        
    @staticmethod #TODO - move it to the right class!
    def copy_file_from_device(source_path,dist_path):
        cmd = "adb pull %s %s" %(source_path,dist_path)
        system(cmd)

    @staticmethod
    def find_max_match_sub_image_in_image(image,sub_image):
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

    @staticmethod
    def ocr_image(image_name, crop_dict):
        image = cv2.imread(ImageTools.DIST_PATH + image_name)
        cropped_image = ImageTools.crop_image(image, crop_dict)
        cropped_path = ImageTools.DIST_PATH + "cropped_image.png"
        cv2.imwrite(cropped_path, cropped_image)
        return pytesseract.image_to_string(Image.open(cropped_path)) 

class matchStats(object):
    def __init__(self,max_value,max_location):
        self.max_value = max_value
        self.max_location = max_location
        
