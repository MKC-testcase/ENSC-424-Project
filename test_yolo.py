"""
By Marcus Chan
tutorial from :
https://www.youtube.com/watch?v=1LCb1PVqzeY&ab_channel=eMasterClassAcademy
adjusted to use yolov4 instead of yolov3
"""
import cv2
import numpy as np

net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
classes = []

with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture('road.mp4')
#image_frame = cv2.imread('kite.jpg')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)


print("frame count: {}".format(length))
print("FPS: {}".format(fps))

for x in range(length):
    _, image_frame = cap.read()
    height, width ,_ = image_frame.shape

    blob = cv2.dnn.blobFromImage(image_frame, 1/255,(416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    print(len(boxes))
    #add in the check if certain classes are here

    for clas in class_ids:

        print(str(classes[class_ids[clas]]))

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0,255,size=(len(boxes), 3))

    if len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(image_frame, (x,y), (x+w, y+h), color, 2)
            cv2.putText(image_frame, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)

    cv2.imshow('Image', image_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release
cv2.destroyAllWindows()