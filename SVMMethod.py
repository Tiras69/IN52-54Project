import cv2
import numpy as np 

import contours as ctr
from string import ascii_lowercase

SIZE = 20
numberOfBins = 16

#Pour écriture manuscrite
def straighten(sourceImg):
    imgMoments = cv2.moments(sourceImg)
    print(imgMoments)
    if abs(imgMoments['mu02']) < 1e-2:
        return sourceImg.copy()
    skew = imgMoments['mu11']/imgMoments['mu02']
    M = np.float32([[1, skew, -0.5*SIZE*skew], [0, 1, 0]])
    print(M)
    straightenedImg = cv2.warpAffine(img,M,(SIZE, SIZE),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR)
    return straightenedImg

def histOfGradient(sourceImg):
    gradientX = cv2.Sobel(sourceImg, cv2.CV_32F, 1, 0)
    gradientY = cv2.Sobel(sourceImg, cv2.CV_32F, 0, 1)
    magnitude, angle = cv2.cartToPolar(gradientX, gradientY)
    
    #print(angle)

    bins = np.int32(numberOfBins * angle/(2*np.pi))
    #print (magnitude)
    
    #dividing in 4 zones the letter
    binZones = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    magnitudeZones = magnitude[:10,:10], magnitude[10:,:10], magnitude[:10,10:], magnitude[10:,10:]
    #print (binZones)
    hists = [np.bincount(b.ravel(), m.ravel(), numberOfBins) for b, m in zip(binZones, magnitudeZones)]
    hist = np.hstack(hists)     # hist is a 64 bit vector (16 + 16 + 16 + 16)
    return hist



img = cv2.imread('teststraighten.png')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('gray_img', gray_img)
#cv2.waitKey(0)
imgToProcess = cv2.resize(gray_img, (SIZE, SIZE), cv2.INTER_CUBIC)
#cv2.imshow('imgToProcess', imgToProcess)
#cv2.waitKey(0)
hist = histOfGradient(imgToProcess)


img1 = cv2.imread('digits.png',0) 
cells = [np.hsplit(row,100) for row in np.vsplit(img1,50)]
train_cells = [ i[:50] for i in cells ]
hogdata = [list(map(histOfGradient,row))for row in train_cells]
print(hogdata)
print(len(hogdata[0][0]))
trainData = np.float32(hogdata).reshape(-1,64)
print(len(trainData[0]))


responses = np.array([i for i in range(0, 26)]).astype(np.float32)
#print(responses)
responses = np.repeat(responses, 20)
#print(responses)
#svm = cv2.ml.SVM()

svm = cv2.ml.SVM_create()
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setType(cv2.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)

samples, responses, ls, rectangles = ctr.CreateBase('BaseminFinal.png')

im = cv2.imread('BaseminFinal.png')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, imGrayTresh = cv2.threshold(imgray,150,255,cv2.THRESH_BINARY)


for rect in rectangles:
        number = imGrayTresh[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
        number = cv2.resize(number, (10, 10))
        hists  = histOfGradient(number)



#print(test[0])
#cv2.imshow('samples', test[25])
#cv2.waitKey(0)



    # we use the same method for the other document we want to test.
#samplesTest, r, linesIndices = ctr.CreateBase('lorem.png')

#for s in samples:
#    histOfGradient(s)
