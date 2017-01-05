import cv2
import numpy as np
import sys
import os

base = cv2.imread('arial.png')
charPath ="chars"

gray_base = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)

#print gray_base.shape
#cv2.imshow('gray', gray_base)
#cv2.waitKey(0)

ret,thres_img = cv2.threshold(gray_base,127,255,cv2.THRESH_BINARY_INV)
#cv2.imshow('thres', thres_img)
#cv2.waitKey(0)

image, contours, hierarchy = cv2.findContours(thres_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rectangles = [cv2.boundingRect(contour) for contour in contours]
i = 0
for rectangle in rectangles:
    # Draw the rectangles
    i = i+1
    #cv2.imshow('rect'+ str(i), base[rectangle[1]:(rectangle[1]+rectangle[3]), rectangle[0]:(rectangle[0]+rectangle[2])])
    #cv2.rectangle(base, (rectangle[0], rectangle[1]), (rectangle[0] + rectangle[2], rectangle[1] + rectangle[3]), (0, 0, 255), 3) 
    print(rectangle)
    #part = 
    #for asc in range (0, 256):
    #	if os.path.isdir(charPath + '/' + str(asc))
    #res = cv2.resize(base[rectangle[1]:(rectangle[1]+rectangle[3]), rectangle[0]:(rectangle[0]+rectangle[2])], (50, 50), cv2.INTER_CUBIC)

    #cv2.imwrite(str(i) + '.png', res)
    #cv2.waitKey(0)

results = []
while (len(rectangles) > 0):
	pom = []
	min = rectangles[len(rectangles)-1]
	for i in range(len(rectangles) - 1, -1, -1):
		if ((rectangles[i][1] < (min[1] + min[3]/2)) and rectangles[i][1] > (min[1] - min[3]/2)):
			pom = pom + [rectangles[i]]
			del rectangles[i]
	results = results + [pom]
print (results)
cv2.imshow('base', base)
cv2.waitKey(0)

folders = os.listdir(charPath)

#for folder in folders:
#            files = os.listdir(charPath + '/' +folder)
#            for file in files:


for i in range(0, len(results)):
    for j in range(0, len(results[i])):
        zone = base[results[i][j][1]:(results[i][j][1]+results[i][j][3]), results[i][j][0]:(results[i][j][0]+results[i][j][2])]
        ROI = cv2.resize(zone, (51, 51), cv2.INTER_CUBIC)
        #cv2.imshow('test', ROI)
        #cv2.waitKey(0)
        for folder in folders:
            files = os.listdir(charPath + '/' +folder)
            for file in files:
                template = cv2.imread(charPath + '/' +folder + '/' + file)
                res = cv2.matchTemplate(ROI, template, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if (min_val < 0.1): 
                    print (str(file))
                    cv2.imshow('analysed',ROI)
                    cv2.waitKey(0)




    