import cv2
import numpy as np


import contours as ctr
from string import ascii_lowercase

NUMBER_OF_CHAR_PER_LINE = 20
NUMBER_OF_CLASS = 26

def templateMatching(base, test):
    imBase = cv2.imread(base)
    imTest = cv2.imread(test)

    samples, responses, ls, sp, rectangles= ctr.CreateBase(base)

    # we use the same method for the other document we want to test.
    samplesTest, r, linesIndices, spaces, rectanglesTest = ctr.CreateBase(test)

    indResponses = np.empty((0, 36))
    indResponses = np.append(indResponses, [i for i in ascii_lowercase])

    results = []

    for rectT in rectanglesTest:
        zone = imTest[rectT[1]: (rectT[1] + rectT[3]), rectT[0]: (rectT[0] + rectT[2])]
        ROI = cv2.resize(zone, (21, 21), cv2.INTER_CUBIC)
        #cv2.imshow('zone', ROI)
        #cv2.waitKey(0)
        first = True
        tempMinVal = None
        tmpTemplate = None
        templateIdx = None
        for idx, rect in enumerate(rectangles):
            template = imBase[rect[1]: (rect[1] + rect[3]), rect[0]: (rect[0] + rect[2])]
            templateResized = cv2.resize(template, (20, 20), cv2.INTER_CUBIC)
            res = cv2.matchTemplate(ROI, templateResized, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if first == True:
                tempMinVal = min_val
                tmpTemplate = template
                templateIdx = idx
                first = False
            elif min_val < tempMinVal:
                tempMinVal = min_val
                tmpTemplate = template
                templateIdx = idx
        results.append(int(templateIdx//NUMBER_OF_CHAR_PER_LINE))
        #cv2.imshow('analysed',zone)
        #cv2.waitKey(0)
        #cv2.imshow('found',tmpTemplate)
        #cv2.waitKey(0)
                

    finalString = ''
    for res in range(len(results)):
        if res in spaces:
            finalString = finalString+' '
        if res in linesIndices:
            finalString = finalString+'\n'
        finalString = finalString+indResponses[results[res]]

    print (finalString)
    return finalString

templateMatching('BaseminFinal.png', 'lorem.png')