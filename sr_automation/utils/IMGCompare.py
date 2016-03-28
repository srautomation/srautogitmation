from PIL import Image
import os

#Function that recieves 2 screenshots and compares them to each other.

class IMGCompare(object):
        
    def image_compare(self, imageA, imageB):
        screenshotName = os.path.basename(imageA)
        baseline_histogram = Image.open(imageA).histogram()
        imgB = Image.open(imageB)
        w, h = imgB.size

        if screenshotName == 'PhoneApp.png':
            regionBphoneApp = imgB.crop((0, 71, w, h)) 
            return regionBphoneApp.histogram() == baseline_histogram

        elif screenshotName in('AppLauncher.png','Settings.png'):
            regionBapplauncher = imgB.crop((90, 46, w, h))
            return regionBapplauncher.histogram() == baseline_histogram

        elif screenshotName == 'pcmanfm.png':
            regionBpcmanfm = imgB.crop((150, 142, w, h-118))
            return regionBpcmanfm.histogram() == baseline_histogram

        elif screenshotName == 'Search.png':
            regionBsearch = imgB.crop((80, 68, w-100, h-118))
            return regionBsearch.histogram() == baseline_histogram
    
    def open_image(self,path):
        return Image.open(path)
    
    def compare_image(self, imageA,imageB):
        assert imageA.histogram() == imageB.histogram()
