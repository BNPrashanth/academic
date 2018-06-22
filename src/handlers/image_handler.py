import urllib.request
import cv2
import numpy as np
from image_module import execute


class ImageHandler:

    def main(self, url_list):
        image_list = []
        for url in url_list:
            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            image_list.append(image)

        for image in image_list:
            pr_knife = self.predict_appropriateness("knife", image)
            pr_gun = self.predict_appropriateness("gun", image)
            pr_blood = self.predict_appropriateness("blood", image)
            pr_nudity = self.predict_appropriateness("nudity", image)

            if pr_knife or pr_gun or pr_blood or pr_nudity:
                return 0
        return 1

    @staticmethod
    def predict_appropriateness(classifier, image):
        cls = execute.run_classifier(classifier, image)
        if cls == 0:
            if classifier == "knife":
                print("Knife Found..")
                # Checking for Other Items..
            if classifier == "gun":
                print("Gun Found..")
            if classifier == "blood":
                print("Blood Found..")
            if classifier == "nudity":
                print("Nudity Found..")
        else:
            return False
