import numpy as np
import cv2
from string import ascii_lowercase

def CreateBase(filename):
    im = cv2.imread(filename)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    verticalRectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))
    erode = cv2.erode( imgray, verticalRectKernel)


    ret,thresh = cv2.threshold(erode,200,255,cv2.THRESH_BINARY)
    ret, imGrayTresh = cv2.threshold(imgray,200,255,cv2.THRESH_BINARY)

    im2,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    rectangles = [cv2.boundingRect(contour) for contour in contours]

    #drawRectangles(im, rectangles)
    #cv2.imshow('coutours', im)
    #cv2.waitKey()


    # we want to find rect that are inside other rectangle (we don't want them)
    # but first we need to find the biggest rect and remove it.
    biggestRect = rectangles[0]
    for rect in rectangles:
        if(rectArea(biggestRect) < rectArea(rect)):
            biggestRect = rect

    rectangles.remove(biggestRect)

    removeList = []
    for rect in range(len(rectangles)-1):

        for testRect in range(rect+1, len(rectangles)):
            uRect = unionRect(rectangles[rect], rectangles[testRect])
            if rectEqualrect(rectangles[rect], uRect):
                removeList.append(rectangles[testRect])
            elif rectEqualrect(rectangles[testRect], uRect):
                removeList.append(rectangles[rect])

    # get unique rectangles
    setRemoveList = set(removeList)
    for removeItem in setRemoveList:
        rectangles.remove(removeItem)


    drawRectangles(im, rectangles)
    # cv2.imshow('coutours', im)
    # cv2.waitKey()

    # at the end of this algorithm we have the differents rectangles
    # we sort all rectangle by height
    rectangles.sort(key=lambda x: x[1])
    # we know that the first 20 are a etc..
    samples = []# np.empty((0, len(rectangles)))
    for rect in rectangles:
        number = imGrayTresh[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        number = cv2.resize(number, (20, 20))
        number = number.reshape((1, 20*20))

        samples.append(np.array(number[0]).astype(np.float32))

    print (samples)

    samples = np.array(samples)

    # samples = np.array(samples)

    # print (samples)
    print('coucou')
    print(type(samples))
    print ('coucou2')
    print (type(samples[0]))
    print ('coucou3')
    print type(samples[0][0])



    # responses
    # responses = np.empty((0, 36))
    # responses = np.append(responses, [i for i in ascii_lowercase])
    # responses = np.append(responses, [str(i) for i in range(0, 10)])
    responses = np.array([i for i in range(0, 36)]).astype(np.float32)
    responses = np.repeat(responses, 20)


    print(len(samples))
    print (len(responses))

    return samples, responses


def drawRectangles(image, rectangles):
    for rect in rectangles:
        cv2.rectangle(image, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255), 1)

def unionRect(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return (x, y, w, h)

def rectEqualrect(a,b):
    if a[0] == b[0] and a[1] == b[1] and a[2] == b[2] and a[3] == b[3]:
        return True
    else:
        return  False

def rectArea(a):
    return a[2]*a[3]
