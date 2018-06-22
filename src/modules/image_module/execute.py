from skimage.io import imread
import pickle
from image_module import feature
import os
import numpy as np


knife_model = pickle.load(open("knife_model.pkl", 'rb'))
gun_model = pickle.load(open("gun_model.pkl", 'rb'))
blood_model = pickle.load(open("blood_model.pkl", 'rb'))
adult_model = pickle.load(open("adult_model.pkl", 'rb'))
cake_model = pickle.load(open("cake_model.pkl", 'rb'))
bread_model = pickle.load(open("bread_model.pkl", 'rb'))
cutlery_model = pickle.load(open("cutlery_model.pkl", 'rb'))
police_model = pickle.load(open("police_model.pkl", 'rb'))


def main():
    path = "C:/Users/pavilion/PycharmProjects/Final_TT/dataset/test/"
    ims = os.listdir(path)
    for i in range(len(ims)):
        image = imread(path + ims[i])
        cls1 = run_classifier("knife", image)
        cls2 = run_classifier("gun", image)
        # cls3 = run_blood(image)

        print(ims[i] + " ==>> " + str(cls1) + " " + str(cls2))


def run_classifier(classifier, image):
    model = ""
    data = []
    if classifier == "knife":
        model = knife_model
        data = feature.get_HOG(image)
    elif classifier == "gun":
        model = gun_model
        data = feature.get_HOG(image)
    elif classifier == "nudity":
        data = feature.get_BOW(image)
    elif classifier == "blood":
        data = image
    elif classifier == "cake":
        model = cake_model
        data = feature.get_phog_features(image)
    elif classifier == "bread":
        model = bread_model
        data = feature.get_phog_features(image)
    elif classifier == "cutlery":
        model = cutlery_model
        data = feature.get_phog_features(image)
    elif classifier == "police":
        model = police_model
        data = feature.get_phog_features(image)

    im_shape = np.array(data)
    cls = model.predict(im_shape.reshape(1, im_shape.shape[0]))
    return cls[0]
