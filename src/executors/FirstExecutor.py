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
from components.Package.src.utils.response import build_response
from components.Package.src.models.PackageModel import PackageModel

class Executor1(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        self.mode = self.request.get_param("Operation")
        self.inputImage = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def flip(self, image):
        return cv2.flip(image, 1)

    def run(self):
        img = Image.get_frame(img=self.inputImage, redis_db=self.redis_db)
        
        if self.mode:
            option_name = self.mode.get("name")
            
            if option_name == "Grayscale":
                # ✅ Access the new direct attributes
                text_param = self.mode.get("grayscaleText", {}).get("value", "default")
                number_param = self.mode.get("grayscaleNumber", {}).get("value", 50)
                print(f"Grayscale: text={text_param}, number={number_param}")
                img.value = self.gray(img.value)
                
            elif option_name == "Flip Horizontal":
                # ✅ Access the new direct attributes
                enable_param = self.mode.get("flipEnable", {}).get("value", True)
                mode_param = self.mode.get("flipMode", {}).get("value", "Mode1")
                print(f"Flip: enable={enable_param}, mode={mode_param}")
                if enable_param:
                    img.value = self.flip(img.value)
        
        img = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        self.image = img
                
        return build_response(context=self)

    if "__main__" == __name__:
        Executor(sys.argv[1]).run()