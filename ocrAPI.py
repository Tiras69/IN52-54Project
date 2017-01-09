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

from pylatex import Document, Section, Command
from pylatex.utils import NoEscape



def createTex(docFile, resultOCR):
    docFile.preamble.append(Command('title', 'OCR Result'))
    docFile.preamble.append(Command('author', getpass.getuser()))
    docFile.preamble.append(Command('date', NoEscape(r'\today')))
    docFile.append(NoEscape(r'\maketitle'))

    with docFile.create(Section('Result')):
        docFile.append(resultOCR)


def generatePDF(pdfPath, resultOCR):
    docFile = Document('basic')

    createTex(docFile, resultOCR)

    docFile.generate_pdf(clean_tex = False, filepath = pdfPath)


def generateTXT(txtPath, resultOCR):
    txtFile = open(txtPath + ".txt", 'w')

    txtFile.write(resultOCR)

    txtFile.close()