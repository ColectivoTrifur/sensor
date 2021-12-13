import cv2
from cvzone.HandTrackingModule import HandDetector
import random

from pythonosc import udp_client

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

magenta = (255, 0, 255)
offset = 0

ip="127.0.0.1" #"The ip of the OSC server")
port=8000
start="/play"
stop="/stop"
volume_up="/master/volume"
volume_down="/master/volume"
eq="/eq/type/1"
actions = [start,stop,volume_up,volume_down,eq]
client = udp_client.SimpleUDPClient(ip, port)

class DragRect():
    def __init__(self, *, pos_center, color=magenta, size=[100,100], action=start,name=None):
        self.pos_center = pos_center
        self.size = size
        self.color = magenta
        self.action = action
        self.name = name

    def update(self,cursor,color):
        cx,cy = self.pos_center
        width,height = self.size
        if(
            cx - width // 2 < cursor[0] < cx + width // 2
            and cy - height // 2 < cursor[1] < cy + height // 2
        ):
            self.pos_center = cursor
            self.color = color
            print(self.name, " activated. Sending: ", self.action)
            msg=rect.action
            if msg == volume_down:
                number_sent = 0
            else:
                number_sent = random.randrange(0,9)
            client.send_message(msg, number_sent)
            print(f'OSC MSG sent {number_sent} to {ip}:{port}{msg}')

rects = []
for x in range(5):
    rect = DragRect(pos_center=[x*250+100,100], action=actions[x], name=str(x))
    rects.append(rect)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)
    if lmList:

        # l,_,_ = detector.findDistance(8,12,img)
        l, _, _ = detector.findDistance(4, 8, img)
        cursor = lmList[8]
        if (l < 40):
            colorR = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for rect in rects:
                rect.update(cursor, color=colorR)
                #number_sent = float(l/20)
        else:
            colorR = magenta
            offset = 0
            #msg=stop
            #client.send_message(stop, 0.1)
            #print(f'OSC MSG sent to {ip}:{port}{msg}')
    for rect in rects:
        cx,cy = rect.pos_center
        width,height = rect.size
        cv2.rectangle(
            img,
            (cx - width // 2, cy - height // 2),
            (offset + cx + width // 2, offset + cy + height // 2),
            rect.color,
            cv2.FILLED,
        )
    cv2.imshow("Image", img)
    cv2.waitKey(1)

