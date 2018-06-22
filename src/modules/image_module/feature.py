from skimage.feature import hog
from skimage import io, color, img_as_ubyte, feature
from skimage.feature import greycomatrix, greycoprops
from sklearn.metrics.cluster import entropy
from scipy import ndimage
import numpy as np
import cv2
import math
from sklearn.feature_extraction import image as im


def get_HOG(image):
    image = cv2.resize(image, (200, 200))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gg = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(3, 3), block_norm='L1-sqrt',
             visualise=True, transform_sqrt=False, feature_vector=True)
    return gg[0]


def get_BOW(image):
    pass


def get_texture(output):
    # texture Feature
    grayImg = img_as_ubyte(color.rgb2gray(output))
    #"distances" is a list of distances (in pixels) between the pixels being compared
    distances = [1, 2, 3]
    #"angles" is a list of angles (in radians) between pixels being compared
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    # properties = ['energy', 'homogeneity']

    glcm = greycomatrix(grayImg,
                        distances=distances,
                        angles=angles,
                        symmetric=True,
                        normed=True)
    # feature1 for texture
    contrast = greycoprops(glcm, prop='contrast')
    # feature2 for texture
    energy = greycoprops(glcm, prop='energy')
    # feature3 for texture
    correlation = greycoprops(glcm, prop='correlation')
    # entropy=shannon_entropy(glcm)
    # feature4 for texture
    ent = entropy(glcm)
    # entropy = shannon_entropy(glcm, base=np.e)
    return contrast, energy, correlation, ent


def get_blood_feature(images):
    x = []
    for image in images:
        image = cv2.resize(image, (200, 200))
        features = []
        boundaries = [
            ([0, 0, 120], [50, 80, 255])
        ]

        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)
            l, m, n, o = get_texture(output)
            b, g, r = cv2.split(output)
            b = np.array(b, dtype=float)
            g = np.array(g, dtype=float)
            r = np.array(r, dtype=float)

            for ar in l:
                for el in ar:
                    features.append(el)
            for ar in m:
                for el in ar:
                    features.append(el)
            for ar in n:
                for el in ar:
                    features.append(el)
            features.append(o)
            for ar in r:
                for el in ar:
                    features.append(el)
            for ar in g:
                for el in ar:
                    features.append(el)
            for ar in b:
                for el in ar:
                    features.append(el)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            phog_feature = get_phog_features(image)
        x.append(features)
    return x


# def get_PHOG(image):

def check_for_face(image):
    faceCascade = cv2.CascadeClassifier(
        'C:/Users/pavilion/PycharmProjects/sample1/image/haarcascade_frontalface_default.xml')
    face = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        face,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)
    count1 = 0
    # img1 = skin1[faces[0]:faces[0]+faces[2]][faces[1]:faces[1]+faces[3]]
    for x in faces:
        # img1 = skin[faces[0, 1]:(faces[0, 1]+faces[0, 3]), faces[0, 0]:(faces[0, 0]+faces[0, 2])]
        img1 = image[x[1]:(x[1] + x[3]), x[0]:(x[0] + x[2])]
        for y in img1:
            for z in y:
                if not (z[0] == 0 and z[1] == 0 and z[2] == 0):
                    # count1 = count1 + 1
                    z[0] = 0
                    z[1] = 0
                    z[2] = 0
        return image


def get_skin(image):
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")

    # frame = imutils.resize(frame, width=400)
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # converted = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
    skinMask = cv2.inRange(converted, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(image, image, mask=skinMask)
    return skin


def get_skin_ratio(skin):
    # show the skin in the image along with the mask
    #cv2.imshow("images", skin)
    #cv2.waitKey(0)
    h, w, channel = skin.shape
    total_pixel = h * w
    total_skin = 0
    for py in range(0, h):
        for px in range(0, w):
            # print(skin[py][px])
            if not (skin[py][px][0] == 0 and skin[py][px][1] == 0 and skin[py][px][2] == 0):
                total_skin = total_skin + 1
    #############################################################
    total_skin_ratio = (total_skin / total_pixel) * 100
    return total_skin_ratio


def check_spiral(skin,h,w,total_skin):
    # rows, cols ,channel= skin1.shape
    centralImg = skin[int(h / 3):int(2 * h / 3), int(w / 3):int(2 * w / 3)]

    count = 0
    cv2.imshow("Cropped Top", centralImg)
    cv2.waitKey(0)
    h1, w1, ch = centralImg.shape

    for py in range(0, h1):
        for px in range(0, w1):
            # print(centralImg[py][px])
            if not (centralImg[py][px][0] == 0 and centralImg[py][px][1] == 0 and centralImg[py][px][2] == 0):
                count = count + 1

    ratio = (count / total_skin) * 100

    print("ratio", ratio)
    if ratio < 29:
        print("It is not ponography central skin ratio is lesser than 29%")
    else:
        print("it may be central skin ratio is grater than 29%")


#def get_BOW:


def phog_descriptor(bh, bv, pyramid_levels, bin):
    p = np.empty((0, 1), dtype=int)  # dtype=np.float64? # vertical size 0, horizontal 1

    for b in np.arange(1, bin + 1):
        ind = bh == b
        ind = ind.astype(int)  # convert boolean array to int array
        sum_ind = np.sum(bv[np.where(ind > 0)])
        p = np.append(p, np.array([[sum_ind]]), axis=0)  # append the sum horizontally to empty p array

    cella = 1.
    for l in np.arange(1, pyramid_levels + 1):  # defines a range (from, to, step)
        x = np.fix(np.divide(bh.shape[1], 2. ** l))
        y = np.fix(np.divide(bh.shape[0], 2. ** l))
        xx = 0.
        yy = 0.
        while xx + x <= bh.shape[1]:
            while yy + y <= bh.shape[0]:
                bh_cella = np.array([])
                bv_cella = np.array([])
                bh_cella = bh[int(int(yy + 1.) - 1):int(yy + y), int(int(xx + 1.) - 1):int(xx + x)]
                bv_cella = bv[int(int(yy + 1.) - 1):int(yy + y), int(int(xx + 1.) - 1):int(xx + x)]

                for b in np.arange(1, bin + 1):
                    ind = bh_cella == b
                    ind = ind.astype(int)  # convert boolean array to int array
                    sum_ind = np.sum(bv_cella[np.where(ind > 0)])
                    p = np.append(p, np.array([[sum_ind]]), axis=0)  # append the sum horizontally to p

                yy = yy + y

            cella = cella + 1.
            yy = 0.
            xx = xx + x

    if np.sum(p) != 0:
        p = np.divide(p, np.sum(p))

    return p


def bin_matrix(angle_values, edge_image, gradient_values, angle, bin):

    # 8-orientations/connectivity structure (Matlab's default is 8 for bwlabel)
    structure_8 = [[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]]

    [contorns, n] = ndimage.label(edge_image, structure_8)
    X = edge_image.shape[1]
    Y = edge_image.shape[0]
    bm = np.zeros((Y, X))
    bv = np.zeros((Y, X))
    nAngle = np.divide(angle, bin)
    for i in np.arange(1, n + 1):
        [posY, posX] = np.nonzero(contorns == i)
        posY = posY + 1
        posX = posX + 1
        for j in np.arange(1, (posY.shape[0]) + 1):
            pos_x = posX[int(j) - 1]
            pos_y = posY[int(j) - 1]
            b = np.ceil(np.divide(angle_values[int(pos_y) - 1, int(pos_x) - 1], nAngle))
            if b == 0.:
                bin = 1.
            if gradient_values[int(pos_y) - 1, int(pos_x) - 1] > 0:
                bm[int(pos_y) - 1, int(pos_x) - 1] = b
                bv[int(pos_y) - 1, int(pos_x) - 1] = gradient_values[int(pos_y) - 1, int(pos_x) - 1]

    return [bm, bv]


def phog(image, bin, angle, pyramid_levels):
    angle_values = ""
    grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 0 converts it to grayscale

    bh = np.array([])
    bv = np.array([])
    if np.sum(np.sum(grayscale_img)) > 100.:
        # Matlab The default sigma is sqrt(2); the size of the filter is chosen automatically, based on sigma.
        # Threshold is applied automatically - the percentage is a bit different than in Matlab's implementation:
        # low_threshold: 10%
        # high_threshold: 20%
        edges_canny = feature.canny(grayscale_img, sigma=math.sqrt(2))
        [GradientY, GradientX] = np.gradient(np.double(grayscale_img))
        GradientYY = np.gradient(GradientY)[1]  # Take only the first matrix
        Gr = np.sqrt((GradientX * GradientX + GradientY * GradientY))

        index = GradientX == 0.
        index = index.astype(int)  # Convert boolean array to an int array
        GradientX[np.where(index > 0)] = np.power(10, np.float(-5))
        YX = GradientY / GradientX

        if angle == 180.:
            angle_values = np.divide((np.arctan(YX) + np.pi / 2.) * 180., np.pi)
        if angle == 360.:
            angle_values = np.divide((np.arctan2(GradientY, GradientX) + np.pi) * 180., np.pi)

        [bh, bv] = bin_matrix(angle_values, edges_canny, Gr, angle, bin)
    else:
        bh = np.zeros(image.shape[0], image.shape[1])
        bv = np.zeros(image.shape[0], image.shape[1])

    # Don't consider a roi, take the whole image instead
    bh_roi = bh
    bv_roi = bv
    p = phog_descriptor(bh_roi, bv_roi, pyramid_levels, bin)

    return p


def get_phog_features(image, bins=8, angle=360., pyramid_levels=3):

    feature_vec = phog(image, bins, angle, pyramid_levels)
    feature_vec = feature_vec.T[0]  # Transpose vector, take the first array
    return feature_vec


def get_patches(img):
    img = color.rgb2gray(img)
    trueImg = cv2.resize(img, (64, 64))

    patches = im.extract_patches_2d(trueImg, (16, 16))
    # print(patches.shape)
    # cv2.imshow("pat", patches[2])
    # cv2.waitKey(500)
    X = []
    for patch in patches:
        # meanarr.append(x.mean())
        # stdd.append(x.std())
        # patch = Patch()
        X.append(get_HOG(patch))
    return X
