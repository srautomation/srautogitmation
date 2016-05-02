import sr_tools.config as config
import time
import slash
import cv2
import numpy as np
import Image
import pytesseract
from os import system
from sr_automation.utils.TakeSnapshot import TakeSnapshot
from logbook import Logger
from Tkinter import image_names
log = Logger("ImageTools")

import skimage.measure  

class ImageTools(object):
    SNAPSHOT_PATH = "/tmp/"
    CHROOT_PATH = config.chroot_path
    DIST_PATH = config.automation_files_dir
    
    @staticmethod
    def mse(imageA,imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
    # return the MSE, the lower the error, the more "similar"
    # the two images are
        return err
    
    @staticmethod
    def snap_and_compare(imageName,comparedImagePath,error,threshold=0.9):
        ImageTools.snapShot_and_copy_file(imageName)
        result = ImageTools.compare_images(config.automation_files_dir + imageName, comparedImagePath)
        assert result > threshold , error
    
    @staticmethod
    def compare_images(imageA_path,imageB_path):
        imageA = cv2.imread(imageA_path)
        imageB = cv2.imread(imageB_path)
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY) #convert to greyscale
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY) #convert to greyscale
        s = skimage.measure.structural_similarity(imageA, imageB) # compute SSIM of 2 images
        return s

    @staticmethod
    def find_sub_image_in_image(image_name,subImage_path,crop_boundries=None,needToSnap=True):
        if needToSnap is True:
            ImageTools.snapShot_and_copy_file(image_name)
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
        sub_image_location = np.unravel_index(result.argmax(),result.shape)
        stats = matchStats(maximum,sub_image_location)
        return stats

    @staticmethod
    def crop_image(image,crop_dict):
        cropped_image= image[crop_dict["y_min"]:crop_dict["y_max"], \
                             crop_dict["x_min"]:crop_dict["x_max"], \
                             crop_dict["z_min"]:crop_dict["z_max"] ]
        return cropped_image
    
    @staticmethod
    def snapShot_and_copy_file(image_name,destination=DIST_PATH):
        TakeSnapshot.take_snapshot(ImageTools.SNAPSHOT_PATH, image_name)
        ImageTools.copy_file_from_device(ImageTools.CHROOT_PATH+ImageTools.SNAPSHOT_PATH+image_name,destination )
        
    @staticmethod
    def check_inrange(image,arrayMin,arrayMax):
        image = cv2.imread(image)
        dst = cv2.inRange(image,arrayMin,arrayMax)
        return dst
    
    @staticmethod
    def check_if_black_screen(image):
        ret =  ImageTools.check_inrange(image, np.array([0,0,0],np.uint8),np.array([0,0,0],np.uint8))
        black = cv2.countNonZero(ret)
        return black == ret.size
    
    @staticmethod
    def ocr_image(image_name, crop_dict):
        image = cv2.imread(ImageTools.DIST_PATH + image_name)
        cropped_image = ImageTools.crop_image(image, crop_dict)
        cropped_path = ImageTools.DIST_PATH + "cropped_image.png"
        cv2.imwrite(cropped_path, cropped_image)
        return pytesseract.image_to_string(Image.open(cropped_path)) 

    @staticmethod
    def return_text_on_screen(image_name):
        ImageTools.snapShot_and_copy_file(image_name)
        original = cv2.imread(ImageTools.DIST_PATH + image_name)
        newX,newY= original.shape[1]*2,original.shape[0]*2
        new_image = cv2.resize(original,(newX,newY))
        new_path = ImageTools.DIST_PATH + "resized_image.png"
        cv2.imwrite(new_path, new_image)
        return pytesseract.image_to_string(Image.open(new_path))

class matchStats(object):
    def __init__(self,max_value,max_location):
        self.max_value = max_value
        self.max_location = max_location
        
