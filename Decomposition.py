import numpy as np
import cv2
import Binarization as bnz
from matplotlib import pyplot as plt

def LetterDecomposition():
    image = bnz.binarization2()
    # imageBin = cv2.threshold(image, 127, 1, cv2.THRESH_BINARY)

    # we want just a small circle for complete some letters
    roundCircleKer = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2) )
    dilIM = cv2.erode(image, roundCircleKer, 1)
    cv2.imshow('final result + dil', dilIM)
    cv2.waitKey()

    InvBinIM, dst = cv2.threshold(dilIM, 127, 1, cv2.THRESH_BINARY_INV)

    # the idea between finding all words is to find components
    # each class will be a letter

    # im2, contours, hierarchy, = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(InvBinIM, contours, -1, (0, 255, 0), 1)
    # cv2.imshow('contours', InvBinIM)
    # cv2.waitKey()
    # linesSquareDecompo(InvBinIM)



    # Debug
    #for arr in RectangleArray:
    #    strg = ""
    #    for rect in arr:
    #        strg += str(rect)+", "
    #    print (strg)


def linesSquareDecompo(image):
    # Or we can do the algorithm see in TP
    lineCoord = []
    isInLine = False
    # we take every lines
    for i in range(len(image[1][1])):
        # we count the value of each lines.
        # print (InvBinIM[i+1])
        count = sum(image[1][i])
        if isInLine == False:
            # as 0 means white and 1
            # if the sum of values is more than 0
            # it would said that there's black pixel in the line
            if count > 0:
                isInLine = True
                lineCoord.append(i)
        else:
            if count == 0:
                isInLine = False
                lineCoord.append(i - 1)

    ColumnCoordinates = []

    # now that we have the lines we want to know the differents columns were are the blanks
    for j in range(len(lineCoord) / 2):
        # we take the corresponding matrix:
        workMatrix = []
        for i in range((lineCoord[j * 2 + 1] - lineCoord[j * 2]) + 1):
            workMatrix.append(image[1][i + lineCoord[j * 2]])

        # print ("work matrix "+workMatrix)

        IsInColumn = False
        tmpColumnsArray = []
        # we want to go throught columns
        for columns in range(len(workMatrix[1])):

            # here we will count how many pixel there is in the columns
            # sum() function not avaible as there is no arrays of columns.
            count = 0
            for lines in range(len(workMatrix)):
                count += workMatrix[lines][columns]

            # We want to know were the start and finish of a number
            if IsInColumn == False:
                if count > 0:
                    IsInColumn = True
                    tmpColumnsArray.append(columns)
            else:
                if count == 0:
                    IsInColumn = False
                    tmpColumnsArray.append(columns)

        ColumnCoordinates.append(tmpColumnsArray)

    # here we will begin to create the severals squares around the numbers.
    RectangleArray = []
    for lines in range(len(ColumnCoordinates)):
        tmpRectArray = []
        for columns in range(len(ColumnCoordinates[lines]) / 2):
            tmpRectArray.append(Rectangle(ColumnCoordinates[lines][columns * 2], lineCoord[lines * 2],
                                          ColumnCoordinates[lines][(columns * 2) + 1], lineCoord[(lines * 2) + 1]))
        RectangleArray.append(tmpRectArray)

    # now that we have all the rectangles we can proceed to the OCR part

class Rectangle:

    def __init__(self):
        self.upperLeft = Point()
        self.bottomRight = Point()

    def __init__(self, _ulx, _uly, _brx, _bry):
        self.upperLeft = Point(_ulx, _uly)
        self.bottomRight = Point(_brx, _bry)

    def __str__(self):
        return "Upper left: "+str(self.upperLeft)+" Bottom Right: "+str(self.bottomRight)

class Point:

    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def __str__(self):
        return "x: "+str(self.x)+" y: "+str(self.y)
























LetterDecomposition()
