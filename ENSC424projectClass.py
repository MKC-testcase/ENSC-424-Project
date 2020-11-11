"""
The purpose of this file is to formally transfer what was tested in Yolo test and formally input it into a
easily accessible class
By: Marcus Chan
"""
import cv2
import numpy as np
import os
#from os.path import isfile, join

class media_interpret:
 # This class shall provide the basis of the functions we offer with our project
    def __init__(self):
        self.fps = 0
        self.frame_count = 0
        self.net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
        self.classes = []
        self.boxes = []
        self.class_ids = []
        self.confidences = []
        #variables above help the function of YOLO object determination to run
        self.frame_array = []

    def setupFold(self):
        current_dir = os.getcwd()
        print(current_dir)  # this is also unneeded
        path = current_dir + "/images"
        if not os.path.exists(path):
            os.mkdir(path)
        path = "{}/videos".format(current_dir)
        if not os.path.exists(path):
            os.mkdir(path)

    def readVideo(self, video_name):
        """Input char(video name) to pass into the program"""
        self.vidSetup = False
        try:
            with open('coco.names', 'r') as f:
                self.classes = f.read().splitlines()
            self.cap = cv2.VideoCapture(video_name) #change the road.mp4 to video_name
            self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        except:
            print("Video could not be read please try again")

    def classify_boxes(self):
        """takes the outputs of the yolo system and assigns them the box size, its class and how confident yolo is about the object"""
        self.boxes = []
        self.class_ids = []
        self.confidences = []
        #dimension_storage = []
        for output in self.layerOutputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * self.width)
                    center_y = int(detection[1] * self.height)

                    #dimension_storage.append(detection[2] * self.width)
                    #dimension_storage.append(detection[3] * self.height)
                    #dimension_storage.append(center_x - int(dimension_storage[0] / 2))
                    #dimension_storage.append(center_y - int(dimension_storage[1] / 2))
                    w = int(detection[2] * self.width)
                    h = int(detection[3] * self.height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.boxes.append([x, y, w, h])
                    self.confidences.append(float(confidence))
                    self.class_ids.append(class_id)

    def draw_boxes(self):
        """adds the previously identified objects and the original image frame and adds the frame on top of the image"""
        indexes = cv2.dnn.NMSBoxes(self.boxes, self.confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(len(self.boxes), 3))

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = self.boxes[i]
                label = str(self.classes[self.class_ids[i]])
                confidence = str(round(self.confidences[i], 2))
                color = colors[i]
                cv2.rectangle(self.image_frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(self.image_frame, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

    def image_runthrough(self, object, *args, **kwargs):
        """Runs through the image frame by frame and """
        count  = 0
        vidName = kwargs.get('vidName', None)

        for x in range(self.frame_count):
            #this function runs through all the frames of the image
            self.currentFrame, self.image_frame = self.cap.read()
            self.height, self.width, _ = self.image_frame.shape

            if vidName != None:
                if self.vidSetup == False:
                    try:
                        self.vidSetup = self.vidOption(vidName, int(self.cap.get(3)), int(self.cap.get(4)))
                        print("Saving video as segmented video")
                        self.vidSetup = True
                    except:
                        print("Saving video as individual .jpg images")
                        self.vidSetup = True

            blob = cv2.dnn.blobFromImage(self.image_frame, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
            self.net.setInput(blob)

            output_layers_names = self.net.getUnconnectedOutLayersNames()
            self.layerOutputs = self.net.forward(output_layers_names)
            print(self.layerOutputs)
            self.classify_boxes()
            self.draw_boxes()

            for clas in self.class_ids:
                print(str(self.classes[self.class_ids[clas]]))  # this is to check all the classes in considered
                if object == self.classes[self.class_ids[clas]]:
                    if self.vidSetup == True:
                        self.vid_convert(self.vidSetup)
                        break
                    else:
                        self.acquired_frame(count, 'test2')
                        break
            count = count + 1

            cv2.imshow('Image', self.image_frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

    def acquired_frame(self,count, viddir):
        """This function creates and saves the individual frames into a newly created folder (need to keep track)"""
        current_dir = os.getcwd()
        print(current_dir) #this is also unneeded
        path = current_dir + "/images"
        try:
            path = path+ "/"+ viddir
            if not os.path.exists(path):
                os.mkdir(path)
        except:
            print("video directory name was not input correctly")
        print(self.currentFrame)
        if self.currentFrame:
            try:
                #this probably doesn't interact well with duplicate images
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
        if confirm == True:
            self.out.write(self.image_frame)
        else:
            print("You have not enabled the video segmentation option")

     #https://(medi)um.com/@iKhushPatel/convert-video-to-images-images-to-video-using-opencv-python-db27a128a481

    def proper_end(self):
        self.cap.release()
        if self.vidSetup == True:
            self.out.release()

if __name__ == '__main__':
    # input the base sequence here
    test = media_interpret()
    test.setupFold()
    test.readVideo('road.mp4')
    test.image_runthrough('car', vidName='test_vid.avi')
    test.proper_end()

    #for the future purhaps explore the possibility to compress the jpg files automatically --> store as txt file
    #first convert to YUV then get the bit map --> prediction between frames?
    #--> our own compression scheme