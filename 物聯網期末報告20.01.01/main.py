#from subprocess import run

import cv2, time
from requests import get
import numpy as np
############################Define the DNN#####################
#取得輸出層
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

#劃出預測
def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)

#設定label names
classes = None
with open('obj.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
    
cap = cv2.VideoCapture(0)
#COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
COLORS = [(0,0,255),(0,255,255),(0,255,0),(255,0,0),(255,255,0)]

net = cv2.dnn.readNet('yolov3-tiny_last.weights', 'yolov3-tiny.cfg')
####################################################################
#臉部偵測
def detect():
    global running
    ret, image = cap.read()
    image = cv2.flip(image,1) #水平翻轉，使觀看更直覺
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    
    
    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
        
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    emotion = "close"
    for i in indices:
        i = i[0]
        emotion = str(classes[class_ids[i]])
        print(emotion)
        box = boxes[i]
        xxx = box[0]
        yyy = box[1]
        www = box[2]
        hhh = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(xxx), round(yyy), round(xxx+www), round(yyy+hhh))
        
#        if emotion== "neutral":
#            returnx = "r"
#        elif emotion == "sad": 
#            returnx = "r"
#        elif emotion == "angry": #這個不好偵測，但戴上眼鏡都是angry
#            returnx = "g"
#        elif emotion == "happy":
#            returnx = "b"
#        elif emotion == "surprised":
#            returnx = "b"
#        break
    cv2.imshow("Facial Detection", image) #顯示畫面
    k = cv2.waitKey(1)
    if k == 27:running = False
    if k == 32:
        return "close"
    else:return emotion

ip = "192.168.0.15" #填入裝置連到的IP
running = True
while(running):
    a = get("http://"+ ip +"/cmd?led=" + detect())
    time.sleep(0.5)
    
a = get("http://"+ ip +"/cmd?led=close")
quit()