"""
First Executor: image preprocessing (Grayscale or Horizontal Flip).
"""


import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayScaleFlipHorizontal.src.utils.response import build_response
from components.GrayScaleFlipHorizontal.src.models.PackageModel import PackageModel


class FirstExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.mode = self.request.get_param("Operation")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}


    def gray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    def flip(self, img):
        return cv2.flip(img, 1)


    def run(self):
        img=Image.get_frame(img=self.image, redis_db=self.redis_db)

        
        if self.mode:
            option_name = self.mode.get("name")
            
            if option_name == "Grayscale":
                img.value = self.gray(img.value)
            elif option_name == "Flip Horizontal":
                img.value = self.flip(img.value)
                
        
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
       
        
        packageModel = build_response(context=self)    
        return packageModel
            


    if "__main__" == __name__:
        Executor(sys.argv[1]).run()