import numpy
import cv2

import sys
import os
import subprocess
from fontTools.ttLib import TTFont

def TTFtoPNG():
    TEXTS_DIR = "texts"
    IMAGES_DIR = "images"

    TTF_PATH = "arial.ttf"
    FONT_SIZE = 11
    TTF_NAME, TTF_EXT = os.path.splitext(os.path.basename(TTF_PATH))

    # we get the ttf object.
    ttf = TTFont(TTF_PATH)

    #ttf = TTFont(TTF_PATH, 0, verbose=0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)

    # we create the directories
    for d in [TEXTS_DIR, IMAGES_DIR]:
        if not os.path.isdir(d):
            os.mkdir(d)

    # write all caracters in the font to differents files
    for x in ttf["cmap"].tables:
        for y in x.cmap.items():
            char_unicode = chr(y[0])
            char_utf8 = char_unicode.encode('utf_8')
            char_name = y[1]
            with open(os.path.join(TEXTS_DIR, char_name + '.txt'), 'wb') as file:
                file.write(char_utf8)
    ttf.close()

    files = os.listdir(TEXTS_DIR)
    for filename in files:
        name, ext = os.path.splitext(filename)
        input_txt = TEXTS_DIR + "/" + filename
        output_png = IMAGES_DIR + "/" + TTF_NAME + "_" + name + "_" + str(FONT_SIZE) + ".png"
        subprocess.call(["convert", "-font", str(TTF_PATH), "-pointsize", str(FONT_SIZE), "-background", "rgba(0,0,0,0)", "label:@" + input_txt, output_png])

    print("finished")


def addBaseFromTTFFile(fontFile):
    print ("hello")

TTFtoPNG()