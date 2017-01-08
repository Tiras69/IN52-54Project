import numpy as np
import cv2

def CreateBase(filename):
    im = cv2.imread(filename)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    verticalRectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 7))
    erode = cv2.erode( imgray, verticalRectKernel)


    ret,thresh = cv2.threshold(erode,150,255,cv2.THRESH_BINARY)
    ret, imGrayTresh = cv2.threshold(imgray,150,255,cv2.THRESH_BINARY)

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

    # at the end of this algorithm we have the differents rectangles
    # we sort all rectangle by height
    rectangles.sort(key=lambda x: x[1])

    # we want to detect lines
    # so in the first place we get the average height of a letter
    averageH = 0
    for rect in rectangles:
        averageH += rect[3]
    averageH /= len(rectangles)

    # removing ponctuation
    removeList = []
    for rect in rectangles:
        if rect[3] < averageH*3/4:
            removeList.append(rect)

    for item in removeList:
        rectangles.remove(item)

    # now we will detect if between two letters there's a gap higher than the average height
    lineStarts = []
    lineStarts.append(0)
    for i in range(len(rectangles)-1):
        if abs(rectangles[i][1]-rectangles[i+1][1]) > averageH/2:
            lineStarts.append(i+1)

    # sort line by lines
    for i in range(len(lineStarts)):
        if i != len(lineStarts)-1:
            tmpLst = rectangles[lineStarts[i]:lineStarts[i+1]-1]
            tmpLst.sort(key=lambda x: x[0])
            rectangles[lineStarts[i]:lineStarts[i + 1] - 1] = tmpLst
        else:
            tmpLst = rectangles[lineStarts[i]:len(rectangles)-1]
            tmpLst.sort(key=lambda x: x[0])
            rectangles[lineStarts[i]:len(rectangles)-1] = tmpLst

    # in this part we detects blanks between words
    spaces = []
    #detect the average space between letter on a line.
    averageSpace = 0
    finalDiv = 0
    for i in range(len(lineStarts)):
        if i != len(lineStarts)-1:
            tmpRects = rectangles[lineStarts[i]:lineStarts[i+1]]
        else:
            tmpRects = rectangles[lineStarts[i]:len(rectangles)-1]

        for rect in range(len(tmpRects)-1):
            averageSpace += abs((tmpRects[rect][0]+tmpRects[rect][2])-(tmpRects[rect+1][0]))
        finalDiv += len(tmpRects)-1
    averageSpace = averageSpace / finalDiv
    # then we detect every space superior to 1/4 the average.
    for i in range(len(lineStarts)):
        if i != len(lineStarts)-1:
            tmpRects = rectangles[lineStarts[i]:lineStarts[i+1]]
        else:
            tmpRects = rectangles[lineStarts[i]:len(rectangles)-1]

        for rect in range(len(tmpRects)-1):
            spacing = abs((tmpRects[rect][0]+tmpRects[rect][2])-(tmpRects[rect+1][0]))
            if spacing > averageSpace/4:
                spaces.append(lineStarts[i]+rect+1)

    drawRectangles(im, rectangles)
    cv2.imshow('coutours', im)
    cv2.waitKey()

    # we know that the first 20 are a etc..
    samples = []# np.empty((0, len(rectangles)))
    for rect in rectangles:
        number = imGrayTresh[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        number = cv2.resize(number, (10, 10))
        number = number.reshape((1, 10*10))

        samples.append(np.array(number[0]).astype(np.float32))

    samples = np.array(samples)

    # samples = np.array(samples)

    # responses
    # responses = np.empty((0, 36))
    # responses = np.append(responses, [i for i in ascii_lowercase])
    # responses = np.append(responses, [str(i) for i in range(0, 10)])
    responses = np.array([i for i in range(0, 26)]).astype(np.float32)
    responses = np.repeat(responses, 20)

    return samples, responses, lineStarts, spaces, rectangles


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

#CreateBase('BaseminFinal.png')