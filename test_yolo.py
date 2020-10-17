"""
By Marcus Chan
all credit with the YOLO library goes to Preggie
this is sample code to work with YOLO V4 using python version 3.8
from terminal => pip install yolo-v4
then to check out where on your computer where the library are installed
go into the python repl:
import yolov4
globals() # this just check that the repl has the file loaded
help(yolov4) #this chows you the package details, the contents and where it is located on the machine for further
changes that you may wish to make
"""

from yolov4.darknet import *

preprocess = Detector()
test = DarkNetPredictionResult()

preprocess.classify()