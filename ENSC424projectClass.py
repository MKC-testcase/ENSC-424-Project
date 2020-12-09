"""
The purpose of this file is to formally transfer what was tested in Yolo test and formally input it into a
easily accessible class
By: Marcus Chan
Used: https://(medi)um.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481
https://www.youtube.com/watch?v=1LCb1PVqzeY&ab_channel=eMasterClassAcademy
https://www.youtube.com/watch?v=DLngCtsG3bk&feature=emb_logo&ab_channel=eMasterClassAcademy
"""
import cv2
import numpy as np
import os
import math
import shutil
#from os.path import isfile, join

class media_interpret:
 # This class shall provide the basis of the functions we offer with our project
    def __init__(self):
        self.fps = 0
        self.frame_count = 0
        self.net = cv2.dnn.readNet('yolov4-training_8000.weights', 'yolov4-training.cfg')
        self.classes = [] #stores the name classes of the class_ids
        self.boxes = [] #stores the dimenstions of boxes drawn on the image
        self.class_ids = [] #stores the class id (integer) of the objects in frame
        self.confidences = [] #confidences of the object in the frame
        #variables above help the function of YOLO object determination to run
        self.in_frame = [] #this is used for keeping track of beginning and ends of when object is in frame
        self.fobj = False #a flag to indicate when the object is in frame

    def setupFold(self):
        """This function sets up a automatic images and video folder in current folder  """
        current_dir = os.getcwd() #gets current directory
        print(current_dir)  # prints current directory
        path = current_dir + "/images"
        #if images folder doesn't exist create it
        if not os.path.exists(path):
            os.mkdir(path)
        path = "{}/videos".format(current_dir)
        #if video folder doesn't exist create it
        if not os.path.exists(path):
            os.mkdir(path)

    def readVideo(self, video_name):
        """Input char(video name) to pass into the program"""
        self.vidSetup = False
        #try statement in case video is unable to be loaded
        try:
            #reads the names file line by line
            with open('coco.names', 'r') as f:
                self.classes = f.read().splitlines()
            #getting pipeline for video frames
            self.cap = cv2.VideoCapture(video_name)
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) #extract the total number of frames using opencv
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) #extract frame rate using opencv
        except:
            print("Video could not be read please try again")

    def classify_boxes(self):
        """takes the outputs of the yolo system and assigns them the box size, its class and how confident yolo is about the object"""
        #setting up the lists for the classes, confidences and box dimenstions of YOLO
        self.boxes = []
        self.class_ids = []
        self.confidences = []
        dimension_storage = []
        #extract results from Yolo
        for output in self.layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                #if the confidence level is above 50%
                if confidence > 0.5:
                    #based on the upper left corner coordinate derives box dimensions of the object
                    center_x = int(detection[0] * self.width)
                    center_y = int(detection[1] * self.height)
                    dimension_storage = []
                    temp_w = int(detection[2] * self.width)
                    temp_h = int(detection[3] * self.height)
                    dimension_storage.append(center_x - int(temp_w / 2))
                    dimension_storage.append(center_y - int(temp_h / 2))
                    dimension_storage.append(temp_w)
                    dimension_storage.append(temp_h)
                    #appending the dimensions of box to boxes to be drawn later
                    self.boxes.append(dimension_storage)
                    #stores confidences and class_ids for labeling
                    self.confidences.append(float(confidence))
                    self.class_ids.append(class_id)

    def draw_boxes(self):
        """draws boxes onto copy of current frame, with label, returned using self.image_frame"""
        #Uses OpenCv to determine the objects with the highest confidence and sets that to the indexes
        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 0.5, 0.4)
        #assigning font and box color
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(self.boxes), 3))

        #if there are object detected
        if len(indexes) > 0:
            #draws boxes and labels on to copies of the original image through self.image_frame
            for i in indexes.flatten():
                x, y, w, h = self.boxes[i]
                label = str(self.classes[self.class_ids[i]])
                confidence = str(round(self.confidences[i], 2))
                color = colors[i]
                cv2.rectangle(self.image_frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(self.image_frame, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

    def image_runthrough(self, object, *args, **kwargs):
        """Runs through the image frame by frame"""
        count  = 0
        #optional input, if given input returns segmented video, if not returns relevant images in image folder
        vidName = kwargs.get('vidName', None)

        # this function runs through all the frames of the image
        for x in range(self.frame_count):
            #gathers current frame from cap
            self.currentFrame, self.image_frame = self.cap.read()
            #extracts the height and width from captured frame
            self.height, self.width, _ = self.image_frame.shape

            #determines if input was given for video segmentation
            if vidName != None:
                if self.vidSetup == False:
                    try:
                        #calls video enabled function
                        self.vidSetup = self.vidOption(vidName, int(self.cap.get(3)), int(self.cap.get(4)))
                        print("Saving video as segmented video")
                        #makes sure to set up video only once
                        self.vidSetup = True
                    except:
                        #video unwanted returning frame images
                        print("Saving video as individual .jpg images")
                        self.vidSetup = True

            #setting up the image for additions
            blob = cv2.dnn.blobFromImage(self.image_frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
            self.net.setInput(blob)

            #extracting information about the object from Yolo
            output_layers_names = self.net.getUnconnectedOutLayersNames()
            self.layerOutputs = self.net.forward(output_layers_names)
            #determines objects in the box
            self.classify_boxes()
            #draws boxes determined from classify_boxes
            self.draw_boxes()

            #indexes represents the objects in frame, and defaults to the highest confidience of each object
            indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 0.5, 0.4)
            #check if there are objects at all
            if len(indexes) > 0:
                #for each object
                for i in indexes.flatten():
                    #if the specified object is found
                    if object == self.classes[self.class_ids[i]]:
                        #if and else statments here are based on user input,
                        # pending on whether to save as part of a video or image
                        if self.vidSetup == True:
                            #this line actually sends the image to the video
                            self.vid_convert(self.vidSetup)
                            # keeping track of the time frames that object is in frame
                            if self.fobj == False:
                                #object is detected so in_frame and fObj set accordingly
                                self.in_frame.append(x)
                                self.fObj = True
                            break
                        else:
                            self.acquired_frame(count, 'test2')
                            break
                    #if object was found this condition activates when object leaves
                    elif self.fobj == True:
                        #returns when object leaves frame to in_frame and set fObj accordingly
                        self.fobj == False
                        self.in_frame.append(x)
            count = count + 1

            if (x == self.frame_count):
                self.fobj == False
                self.in_frame.append(x)

            #creates a window to watch the segmentation
            cv2.imshow('Image', self.image_frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

    def acquired_frame(self,count, viddir):
        """This function creates and saves the individual frames into a newly created folder (need to keep track)"""
        #gets the current folder
        current_dir = os.getcwd()
        print(current_dir)
        #if somehow the images folder hasn't been created, create the images folder
        path = current_dir + "/images"
        try:
            path = path+ "/"+ viddir
            if not os.path.exists(path):
                os.mkdir(path)
        except:
            print("video directory name was not input correctly")
        print(self.currentFrame)
        #writes the frame as a image to the folder
        if self.currentFrame:
            try:
                #writing the the image to the folder named based on a count
                os.chdir(path)
                cv2.imwrite("image{}.jpg".format(count), self.image_frame)
                print("Saved Frame {}".format(count))
                os.chdir(current_dir)
            except:
                print("Saving frame {}, has failed".format(count))

    def vidOption(self, vidName, vidwidth, vidheight):
        """This function sets up the conditions for creating the video"""
        self.out = cv2.VideoWriter(vidName, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps,
                                   (vidwidth, vidheight))
        return True

    def vid_convert(self, confirm):
        """This is a different acquired_frame based on the python example of writing to a file for OpenCV"""
        #writing the video frame to the segmented video
        if confirm == True:
            self.out.write(self.image_frame)
        else:
            print("You have not enabled the video segmentation option")

    def output_interest_timestamp(self, txt_file, path):
        count = 0
        #creates new text file to write in
        new_file = open(txt_file, "w+")
        for read in self.in_frame:
            #write to file every other time to record timestamps
            beginning = read
            end = beginning
            count = count + 1
            if (count%2) == 0:
                #configuring frame number to timestamps using fps of original video
                fps1 = math.floor(beginning/self.fps)
                fps2 = math.ceil(end/self.fps)
                sec1 = math.floor(fps1%60)
                min1 = math.floor((fps1/60)%60)
                hour1 = math.floor((fps1/(60*60)))
                sec2 = math.floor(fps2 % 60)
                min2 = math.floor((fps2 / 60) % 60)
                hour2 = math.floor((fps2 / (60 * 60)))
                new_file.write("object of interest in {}:{}:{}--{}:{}:{} \n".format(hour1,min1,sec1,hour2,min2,sec2))
        new_file.close()
        #moving file that was created in current directory to disired directory
        current_dir = os.getcwd()
        new_path = "{}/{}".format(path, txt_file)
        current_dir = "{}/{}".format(current_dir,txt_file)
        shutil.move(current_dir, new_path)

    #releases all of the resourses held by this program
    def proper_end(self):
        self.cap.release()
        if self.vidSetup == True:
            self.out.release()

#this is for calling the class file itself as a program for testing purposes
if __name__ == '__main__':
    # input the base sequence here
    test = media_interpret()
    test.setupFold()
    test.readVideo('road.mp4')
    test.image_runthrough('Deer', vidName='test3_vid.avi')
    test.output_interest_timestamp('test3_vid.txt', 'D:/Marcus/ENSC_424_aspg/ENSC_project_py/ENSC_424_project_Marcus/ENSC-424-Project/videos')
    test.proper_end()
