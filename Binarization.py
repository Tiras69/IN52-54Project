import numpy as np
import cv2
from matplotlib import pyplot as plt


# first try of the binarization
def binarization1(filename):
    img = cv2.imread(filename, 0)

    #cv2.imshow('image origine', img)
    #cv2.waitKey(0)

    #plt.subplot(1, 1, 1), plt.hist(img.ravel(), 256)
    #plt.text('Histogramme')
    #plt.show()

    # Adaptive Gaussian Thresholding + connexite
    im_th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 11, 4)

    print (im_th)
    #cv2.imshow('adaptative gaussian threshold', im_th)
    #cv2.waitKey(0)

    return labelingConnectivity(im_th)

# labeling the pixels with the m_connexity
def labelingConnectivity(image):
    currentLabel = 0;

    # create matrix for each pixel labels -1 means no label
    labelMap = [[-1 for _ in range(len(image[0]))] for _ in range(len(image))]

    # here we define the connexes components with uniques labels
    for i in range(len(image)-1):
        for j in range(len(image[i])-1):
            if image[i][j] == 0 and image[i+1][j] == 0:
                if labelMap[i][j] == -1 and labelMap[i+1][j] == -1:
                    labelMap[i][j] = currentLabel
                    labelMap[i+1][j] = currentLabel
                    currentLabel += 1
                elif labelMap[i][j] == -1 and labelMap[i+1][j] != -1:
                    labelMap[i][j] = labelMap[i+1][j]
                elif labelMap[i][j] != -1 and labelMap[i+1][j] == -1:
                    labelMap[i+1][j] = labelMap[i][j]

            if image[i][j] == 0 and image[i][j+1] == 0:
                if labelMap[i][j] == -1 and labelMap[i][j+1] == -1:
                    labelMap[i][j] = currentLabel
                    labelMap[i][j+1] = currentLabel
                    currentLabel += 1
                elif labelMap[i][j] == -1 and labelMap[i][j+1] != -1:
                    labelMap[i][j] = labelMap[i][j+1]
                elif labelMap[i][j] != -1 and labelMap[i][j+1] == -1:
                    labelMap[i][j+1] = labelMap[i][j]

            if image[i][j] == 0 and image[i+1][j+1] == 0:
                if labelMap[i][j] == -1 and labelMap[i+1][j+1] == -1:
                    labelMap[i][j] = currentLabel
                    labelMap[i+1][j+1] = currentLabel
                    currentLabel += 1
                elif labelMap[i][j] == -1 and labelMap[i+1][j+1] != -1:
                    labelMap[i][j] = labelMap[i+1][j+1]
                elif labelMap[i][j] != -1 and labelMap[i+1][j+1] == -1:
                    labelMap[i+1][j+1] = labelMap[i][j]

            if j > 0 and image[i][j] == 0 and image[i+1][j-1] == 0:
                if labelMap[i][j] == -1 and labelMap[i+1][j-1] == -1:
                    labelMap[i][j] = currentLabel
                    labelMap[i+1][j-1] = currentLabel
                    currentLabel += 1
                elif labelMap[i][j] == -1 and labelMap[i+1][j-1] != -1:
                    labelMap[i][j] = labelMap[i+1][j-1]
                elif labelMap[i][j] != -1 and labelMap[i+1][j-1] == -1:
                    labelMap[i+1][j-1] = labelMap[i][j]

    # for each classes we count the number of pixels
    classes = [0 for _ in range(currentLabel)]
    for i in range(len(image)-1):
        for j in range(len(image[i])-1):
            if labelMap[i][j] != -1:
                classes[labelMap[i][j]] += 1

    # we get the average values of all classes
    moy = 0
    for values in classes:
        moy += values
    moy /= currentLabel

    print ('moy '+str(moy))

    # we delete all "small classes" inferior to the average
    for i in range(len(image)-1):
        for j in range(len(image[i])-1):
            if classes[labelMap[i][j]] < moy*3/4:
                image[i][j] = 255


    # image threshold minus little classes
    #cv2.imshow('final result', image)
    #cv2.waitKey(0)
    return image

def binarization2(filename):
    img = cv2.imread(filename, 0)

    # Get the Blurred Image
    img_blur = cv2.blur(img, (5,5))

    # Getting the corresponding threshold images
    img_blur_th = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                        cv2.THRESH_BINARY, 11, 3)

    # dilating results
    # kernel
    ker = np.ones((5,5),np.uint8)
    img_blur_th_morph = cv2.morphologyEx(img_blur_th, cv2.MORPH_OPEN, ker)

    img_th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                        cv2.THRESH_BINARY, 11, 2)

    # return bluredMask(img_th, img_blur_th_morph)
    bluredMask(img_th, img_blur_th_morph)


def bluredMask(image, blurred_Image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if blurred_Image[i][j] == 255:
                image[i][j] = 255

    cv2.imwrite("res/cameraGetFrame.png", image)
    # return image
