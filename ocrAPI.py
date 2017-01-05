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

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape



def createTex(docFile, resultTxt):
    docFile.preamble.append(Command('title', 'OCR Result'))
    docFile.preamble.append(Command('author', getpass.getuser()))
    docFile.preamble.append(Command('date', NoEscape(r'\today')))
    docFile.append(NoEscape(r'\maketitle'))

    with docFile.create(Section('Result 1')):
        docFile.append(resultTxt)


def generatePDF(pdfPath, resultTxt):
    savePath = pdfPath.rsplit(".", 1)[0]

    docFile = Document('basic')
    createTex(docFile, resultTxt)

    docFile.generate_pdf(clean_tex = False, filepath = savePath)





