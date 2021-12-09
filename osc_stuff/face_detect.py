import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import random

from pythonosc import udp_client

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
hand_detector = HandDetector(detectionCon=0.8)
face_detector = FaceDetector()

magenta = (255, 0, 255)
colorR = magenta
cx, cy = 100, 100
width, height = 100, 100
offset = 0

ip="127.0.0.1" #"The ip of the OSC server")
port=9001
#channel2="/objects/texturedMesh.002/modifiers/Screw/angle"
#channel="/objects/texturedMesh.002/modifiers/Screw/screw_offset"
channels=["/objects/texturedMesh.001/modifiers/Wireframe/thickness"]
client = udp_client.SimpleUDPClient(ip, port)


while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    img,bboxs = face_detector.findFaces(img)
    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
        number_sent = int(str(bboxs[0]["score"])[4])*.01
        choice = random.choice(channels)
        client.send_message(choice, number_sent)
        print(f'OSC MSG sent {number_sent} to {ip}:{port}/{choice}')
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)
