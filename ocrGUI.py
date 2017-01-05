# -*- coding: utf-8 -*-

import sys
import os
import io
import numpy
import pprint
import getpass
import threading
import logging
import time
import re
import json
import random
import functools
import cv2
import importlib

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import ocrAPI
importlib.reload(ocrAPI)

# How to call the ocrAPI functions :
# ocrAPI.test()



class ocrGUI(QWidget):
    def __init__(self):
        super(ocrGUI, self).__init__()

        self.lastDatabasePath = ""
        self.lastTestImagePath = ""
        self.lastExportResultPath = ""
        self.cameraStop = False;
        self.cameraFeed = ""

        self.ppSetting = pprint.PrettyPrinter(indent=4)
        
        self.initUI()

            
    def initUI(self):
        #------------------------------------------------------------------------------------
        #------------------------------ Widgets declaration  --------------------------------
        #------------------------------------------------------------------------------------

        self.ocrTabWidget = QTabWidget(self)

        self.basicTab = QWidget()
        self.cameraTab = QWidget()
        self.optionTab = QWidget()

        self.baseGrid = QGridLayout()
        self.basicGrid = QGridLayout(self.basicTab)
        self.cameraGrid = QGridLayout(self.cameraTab)
        self.optionGrid = QGridLayout(self.optionTab)

        self.basicDatabaseButton = QPushButton("BROWSE")
        self.basicTestImageButton = QPushButton("BROWSE")
        self.basicExportResultButton = QPushButton("BROWSE")
        self.basicComputeButton = QPushButton("COMPUTE BASIC CHARACTERS RECOGNITION")
        self.cameraDatabaseButton = QPushButton("BROWSE")
        self.cameraStartButton = QPushButton("START CAMERA CAPTURE")
        self.cameraGetButton = QPushButton("GET CAMERA FRAME")
        self.cameraStopButton = QPushButton("STOP CAMERA CAPTURE")
        self.cameraExportResultButton = QPushButton("BROWSE")
        self.cameraComputeButton = QPushButton("COMPUTE CAMERA CHARACTERS RECOGNITION")

        self.basicDatabaseLabel = QLabel("Database :")
        self.basicTestImageLabel = QLabel("Test Image :")
        self.basicExportResultLabel = QLabel("Result Export :")
        self.cameraDatabaseLabel = QLabel("Database :")
        self.cameraPreviewLabel = QLabel()
        self.cameraExportResultLabel = QLabel("Result Export :")

        self.basicDatabaseLineEdit = QLineEdit()
        self.basicTestImageLineEdit = QLineEdit()
        self.basicExportResultLineEdit = QLineEdit()
        self.cameraDatabaseLineEdit = QLineEdit()
        self.cameraExportResultLineEdit = QLineEdit()

        self.menuBar = QMenuBar()

        self.fileMenu = QMenu("File")
        self.optionMenu = QMenu("Options")
        self.helpMenu = QMenu("Help")

        self.quitAction = QAction("Quit", self.fileMenu)
        self.aboutAction = QAction("About", self.helpMenu)

        self.cameraGetPixmap = QPixmap("res/cameraPlaceholder.png")
        self.resultPlaceholderPixmap = QPixmap("res/resultPlaceholder.png")

        #------------------------------------------------------------------------------------
        #----------------------------- Widgets configuration  -------------------------------
        #------------------------------------------------------------------------------------
        
        self.fileMenu.addAction(self.quitAction)
        self.helpMenu.addAction(self.aboutAction)

        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.optionMenu)
        self.menuBar.addMenu(self.helpMenu)

        if not self.cameraGetPixmap.isNull() :
            self.cameraPreviewLabel.setPixmap(self.cameraGetPixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.FastTransformation))

        self.aboutText = "IN52/54 OCR\n\n"
        self.aboutText += "This OCR's objective is to scan an input image, be it a .png image provided by the user, or an image from a webcam.\n"
        self.aboutText += "The data contained in the image are then compared to a database provided by the user. The result will be exported in a .txt file.\n"
        self.aboutText += "\n\nBy ALLIOT Renaud, BEDIR Sibel, JEAN Constantin, METGE Mathieu and SENOUF Joshua."

        self.cameraStartButton.setEnabled(True)
        self.cameraGetButton.setEnabled(False)
        self.cameraStopButton.setEnabled(False)

        #------------------------------------------------------------------------------------
        #------------------------------ Connects declaration  -------------------------------
        #------------------------------------------------------------------------------------

        self.quitAction.triggered.connect(self.close)
        self.aboutAction.triggered.connect(self.openAbout)

        self.basicDatabaseButton.clicked.connect(functools.partial(self.databaseBrowse, self.basicDatabaseLineEdit))
        self.basicTestImageButton.clicked.connect(functools.partial(self.testImageBrowse, self.basicTestImageLineEdit))
        self.basicExportResultButton.clicked.connect(functools.partial(self.exportResultBrowse, self.basicExportResultLineEdit))
        self.cameraDatabaseButton.clicked.connect(functools.partial(self.databaseBrowse, self.cameraDatabaseLineEdit))
        self.cameraExportResultButton.clicked.connect(functools.partial(self.exportResultBrowse, self.cameraExportResultLineEdit))

        self.cameraStartButton.clicked.connect(self.startCaptureCV)
        self.cameraGetButton.clicked.connect(self.getCaptureCV)
        self.cameraStopButton.clicked.connect(self.stopCaptureCV)

        self.basicComputeButton.clicked.connect(self.openResult)
        self.cameraComputeButton.clicked.connect(self.openResult)

        #------------------------------------------------------------------------------------
        #-------------------------- Assign widgets to their layout --------------------------
        #------------------------------------------------------------------------------------

        self.ocrTabWidget.addTab(self.basicTab, "Basic Mode")
        self.ocrTabWidget.addTab(self.cameraTab, "Camera Mode")
        self.ocrTabWidget.addTab(self.optionTab, "Options")

        self.basicGrid.addWidget(self.basicDatabaseLabel, 0, 0, 1, 1)
        self.basicGrid.addWidget(self.basicDatabaseLineEdit, 0, 1, 1, 1)
        self.basicGrid.addWidget(self.basicDatabaseButton, 0, 2, 1, 1)
        self.basicGrid.addWidget(self.basicTestImageLabel, 1, 0, 1, 1)
        self.basicGrid.addWidget(self.basicTestImageLineEdit, 1, 1, 1, 1)
        self.basicGrid.addWidget(self.basicTestImageButton, 1, 2, 1, 1)
        self.basicGrid.addWidget(self.basicExportResultLabel, 2, 0, 1, 1)
        self.basicGrid.addWidget(self.basicExportResultLineEdit, 2, 1, 1, 1)
        self.basicGrid.addWidget(self.basicExportResultButton, 2, 2, 1, 1)
        self.basicGrid.addWidget(self.basicComputeButton, 3, 0, 1, 3)

        self.cameraGrid.addWidget(self.cameraDatabaseLabel, 0, 0, 1, 1)
        self.cameraGrid.addWidget(self.cameraDatabaseLineEdit, 0, 1, 1, 1)
        self.cameraGrid.addWidget(self.cameraDatabaseButton, 0, 2, 1, 1)
        self.cameraGrid.addWidget(self.cameraStartButton, 1, 0, 1, 1)
        self.cameraGrid.addWidget(self.cameraGetButton, 1, 1, 1, 1)
        self.cameraGrid.addWidget(self.cameraStopButton, 1, 2, 1, 1)
        self.cameraGrid.addWidget(self.cameraPreviewLabel, 2, 0, 1, 3)
        self.cameraGrid.addWidget(self.cameraExportResultLabel, 3, 0, 1, 1)
        self.cameraGrid.addWidget(self.cameraExportResultLineEdit, 3, 1, 1, 1)
        self.cameraGrid.addWidget(self.cameraExportResultButton, 3, 2, 1, 1)
        self.cameraGrid.addWidget(self.cameraComputeButton, 4, 0, 1, 3)

        self.baseGrid.addWidget(self.ocrTabWidget, 0, 0, 1, 1)
        self.baseGrid.setMenuBar(self.menuBar)

        self.resize(600, 550)
        self.setLayout(self.baseGrid)
        self.setWindowTitle("IN52/54 OCR")


    def openResult(self):
        self.resultWindow = QWidget()
        self.resultWindowGrid = QGridLayout()
        self.resultWindowLabel = QLabel()
        self.resultWindowTxtButton = QPushButton("EXPORT TO TXT")
        self.resultWindowPdfButton = QPushButton("EXPORT TO PDF")

        if not self.resultPlaceholderPixmap.isNull() :
            self.resultWindowLabel.setPixmap(self.resultPlaceholderPixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.resultWindowGrid.addWidget(self.resultWindowLabel, 0, 0, 1, 2)
        self.resultWindowGrid.addWidget(self.resultWindowTxtButton, 1, 0, 1, 1)
        self.resultWindowGrid.addWidget(self.resultWindowPdfButton, 1, 1, 1, 1)

        testTxt = "C'est une belle journée, je vais me coucher..."

        self.resultWindowPdfButton.clicked.connect(functools.partial(ocrAPI.generatePDF, self.basicExportResultLineEdit.text(), testTxt))

        self.resultWindow.setWindowModality(Qt.ApplicationModal);        
        self.resultWindow.setLayout(self.resultWindowGrid)
        self.resultWindow.resize(640, 480)
        self.resultWindow.setWindowTitle("RESULT")
        self.resultWindow.show()


    def openAbout(self):
        self.aboutWindow = QWidget()
        self.aboutWindowTextEdit = QTextEdit()
        self.aboutWindowGrid = QGridLayout()

        self.aboutWindowTextEdit.setReadOnly(True)
        self.aboutWindowTextEdit.setText(self.aboutText)
        self.aboutWindowGrid.addWidget(self.aboutWindowTextEdit, 0, 0, 0, 0)

        self.aboutWindow.setWindowModality(Qt.ApplicationModal);        
        self.aboutWindow.setLayout(self.aboutWindowGrid)
        self.aboutWindow.setFixedSize(500, 200)
        self.aboutWindow.setWindowTitle("About")
        
        self.aboutWindow.show()


    def databaseBrowse(self, targetWidget, buffer = None):
        databaseName = QFileDialog.getOpenFileName(self,"Select your database file", self.lastDatabasePath if self.lastDatabasePath else QDir.homePath(), "Images files (*.jpg *.png);;All files (*)")

        if databaseName[0]:
            self.lastDatabasePath = databaseName[0].rsplit("/", 1)[0]
            return targetWidget.setText(databaseName[0])


    def testImageBrowse(self, targetWidget, buffer = None):
        testImageName = QFileDialog.getOpenFileName(self,"Select your test image file", self.lastTestImagePath if self.lastTestImagePath else QDir.homePath(), "Images files (*.jpg *.png);;All files (*)")

        if testImageName[0]:
            self.lastTestImagePath = testImageName[0].rsplit("/", 1)[0]
            return targetWidget.setText(testImageName[0])


    def exportResultBrowse(self, targetWidget, buffer = None):
        exportResultName = QFileDialog.getSaveFileName(self,"Save your export result", self.lastExportResultPath if self.lastExportResultPath else QDir.homePath(), "Text files (*.txt);;All files (*)")

        if exportResultName[0]:
            self.lastExportResultPath = exportResultName[0].rsplit("/", 1)[0]
            return targetWidget.setText(exportResultName[0].rsplit("/", 1)[0] + "/" + exportResultName[0].rsplit("/", 1)[1].split(".", 1)[0] + ".txt")


    def startCaptureCV(self):
        self.cameraStop = False
        self.cameraStartButton.setEnabled(False)
        self.cameraGetButton.setEnabled(True)
        self.cameraStopButton.setEnabled(True)

        self.cameraFeed = cv2.VideoCapture(0)

        while(not self.cameraStop):
            returnValue, currentFrame = self.cameraFeed.read()

            if(returnValue):
                cv2.imshow("OpenCV Camera Feed", currentFrame)
            else:
                print("Cannot read video feed from webcam !")

            if cv2.waitKey(1) == 0:
                break
 

    def getCaptureCV(self):
        returnValue, currentFrame = self.cameraFeed.read()
        cv2.imwrite("res/cameraGetFrame.png", currentFrame)
        self.cameraGetPixmap = QPixmap("res/cameraGetFrame.png")

        self.cameraPreviewLabel.setPixmap(self.cameraGetPixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.FastTransformation))


    def stopCaptureCV(self):
        self.cameraStop = True
        self.cameraStartButton.setEnabled(True)
        self.cameraGetButton.setEnabled(False)
        self.cameraStopButton.setEnabled(False)

        self.cameraFeed.release()
        cv2.destroyAllWindows()



def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ocrGUI()

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()