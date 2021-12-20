import cv2
import mediapipe as mp
import random

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#cap = cv2.VideoCapture("video_0002.mp4")
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
from pythonosc import udp_client
ip="127.0.0.1" #"The ip of the OSC server")
port=8000
start="/play"
stop="/stop"
client = udp_client.SimpleUDPClient(ip, port)

with mp_pose.Pose(
    static_image_mode=False) as pose:
    i=1
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128, 0, 250), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2))
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            non_noise = right_wrist.y < 1 or left_wrist.y < 1
            right_up = right_wrist.y <.4 
            left_up = left_wrist.y <.4 
            if right_up: 
                print(i)
                client.send_message(start, right_wrist.y)
                print("SENT START")
                i+=10
            elif left_up:
                client.send_message("/position/++",i)
                client.send_message("/position/++",i)
                client.send_message("/position/++",i)
                client.send_message(start, right_wrist.y)
                print("SENT START")
            else:
                i=1
                client.send_message("/position", "--")
                client.send_message(stop, right_wrist.y)
                print("SENT STOP")
        cv2.imshow("BUCLE Pose", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
