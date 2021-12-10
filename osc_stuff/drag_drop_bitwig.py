import cv2
from cvzone.HandTrackingModule import HandDetector
import random

from pythonosc import udp_client

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

magenta = (255, 0, 255)
colorR = magenta
cx, cy = 100, 100
width, height = 100, 100
offset = 0

ip="127.0.0.1" #"The ip of the OSC server")
port=8000
start="/play"
stop="/stop"
client = udp_client.SimpleUDPClient(ip, port)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)
    if lmList:

        # l,_,_ = detector.findDistance(8,12,img)
        l, _, _ = detector.findDistance(4, 8, img)
        cursor = lmList[8]
        if (
            l < 40
            and cx - width // 2 < cursor[0] < cx + width // 2
            and cy - height // 2 < cursor[1] < cy + height // 2
        ):
            colorR = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            offset += 0
            cx, cy = cursor  # drag
            number_sent = float(l/20)
            client.send_message(start, number_sent)
            msg=start
            print(f'OSC MSG sent to {ip}:{port}{msg}')
        else:
            colorR = magenta
            offset = 0
            msg=stop
            client.send_message(stop, 0.1)
            print(f'OSC MSG sent to {ip}:{port}{msg}')
    cv2.rectangle(
        img,
        (cx - width // 2, cy - height // 2),
        (offset + cx + width // 2, offset + cy + height // 2),
        colorR,
        cv2.FILLED,
    )
    cv2.imshow("Image", img)
    cv2.waitKey(1)

