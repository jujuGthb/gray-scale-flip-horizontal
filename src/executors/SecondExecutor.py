"""
 Dual Image Processor (Resize or Rotate).
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


class SecondExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.mode = self.request.get_param("ProcessingMode")
        self.image1 = self.request.get_param("inputImage1")  
        self.image2 = self.request.get_param("inputImage2") 

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def resize_image(self, img, scale):
        """Simple resize logic."""
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    def rotate_image(self, img, angle):
        """Simple rotate logic."""
        (h, w) = img.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(img, M, (w, h))

    def run(self):
    
        img1 = Image.get_frame(img=self.image1, redis_db=self.redis_db)
        
        
        if self.image2:
            img2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)
        else:
            # If no second image, duplicate the first one 
            img2 = img1 

       
        if self.mode:
            option_name = self.mode.get("name")

            if option_name == "Resize":
                scale = self.mode.get("value", {}).get("Scale", {}).get("value", 0.5)
                method = self.mode.get("value", {}).get("Method", {}).get("value", "area")
                print(f"Resize: scale={scale}, method={method}")
                
                img1.value = self.resize_image(img1.value, scale)
                img2.value = self.resize_image(img2.value, scale)

            elif option_name == "Rotate":
                enabled = self.mode.get("value", {}).get("Enable", {}).get("value", True)
                angle = self.mode.get("value", {}).get("Angle", {}).get("value", 90)
                print(f"Rotate: enabled={enabled}, angle={angle}")
                
                if enabled:
                    img1.value = self.rotate_image(img1.value, angle)
                    img2.value = self.rotate_image(img2.value, angle)

      
        self.outputImage1 = Image.set_frame(img=img1, package_uID=f"{self.uID}_out1", redis_db=self.redis_db)
        
   
        self.outputImage2 = Image.set_frame(img=img2, package_uID=f"{self.uID}_out2", redis_db=self.redis_db)

        
        packageModel = build_response(context=self)
        return packageModel

    if "__main__" == __name__:
        Executor(sys.argv[1]).run()