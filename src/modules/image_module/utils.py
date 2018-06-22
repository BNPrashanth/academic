from sklearn.model_selection import train_test_split
from skimage.io import imread
import os


def get_data(name):
    path1 = "C:/Users/pavilion/PycharmProjects/Image__TT/Dataset/Preprocessed_" + name + "/"
    trainA = os.listdir(path1)
    print(len(trainA))
    path2 = "C:/Users/pavilion/PycharmProjects/Image__TT/Dataset/Preprocessed_Negetive_" + name +"/"
    trainB = os.listdir(path2)
    print(len(trainB))

    X = []
    Y = []
    for i in range(len(trainA)):
        X.append(imread(path1 + trainA[i]))
        Y.append(1)
    for i in range(len(trainB)):
        X.append(imread(path2 + trainB[i]))
        Y.append(0)

    return train_test_split(X, Y, test_size=0.2)
