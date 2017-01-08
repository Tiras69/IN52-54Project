import cv2
import numpy as np
import sys
import os

import contours as ctr



imBase = cv2.imread('BaseminFinal.png')
imTest = cv2.imread('lorem.png')

samples, responses, ls, sp, rectangles= ctr.CreateBase('BaseminFinal.png')

# we use the same method for the other document we want to test.
samplesTest, r, linesIndices, spaces, rectanglesTest = ctr.CreateBase('lorem.png')

for rectT in rectanglesTest:
    zone = imTest[rectT[1]: (rectT[1] + rectT[3]), rectT[0]: (rectT[0] + rectT[2])]
    ROI = cv2.resize(zone, (21, 21), cv2.INTER_CUBIC)
    #cv2.imshow('zone', ROI)
    #cv2.waitKey(0)
    first = True
    tempMinVal = None
    tmpTemplate = None
    for rect in rectangles:
        template = imBase[rect[1]: (rect[1] + rect[3]), rect[0]: (rect[0] + rect[2])]
        templateResized = cv2.resize(template, (20, 20), cv2.INTER_CUBIC)
        res = cv2.matchTemplate(ROI, templateResized, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if first == True:
            tempMinVal = min_val
            tmpTemplate = template
            first = False
        elif min_val < tempMinVal:
            tempMinVal = min_val
            tmpTemplate = template
 
    cv2.imshow('analysed',zone)
    cv2.waitKey(0)
    cv2.imshow('found',tmpTemplate)
    cv2.waitKey(0)
            

    