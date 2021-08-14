import cv2
import mediapipe as mp
import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
pose=mp_pose.Pose()

ptime,ctime=0,0

counter_flag=0
counter=0

while cap.isOpened():
    success, img = cap.read()
    img=cv2.flip(img,1)
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_RGB)
    mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    if results.pose_landmarks:
        rx_0,ry_0=results.pose_landmarks.landmark[16].x,results.pose_landmarks.landmark[16].y
        rx_1, ry_1 = results.pose_landmarks.landmark[14].x, results.pose_landmarks.landmark[14].y
        rx_2, ry_2 = results.pose_landmarks.landmark[12].x, results.pose_landmarks.landmark[12].y
        r_standard=math.hypot(rx_0-rx_1,ry_0-ry_1)
        r_length=math.hypot(rx_0-rx_2,ry_0-ry_2)

        lx_0, ly_0 = results.pose_landmarks.landmark[15].x, results.pose_landmarks.landmark[15].y
        lx_1, ly_1 = results.pose_landmarks.landmark[13].x, results.pose_landmarks.landmark[13].y
        lx_2, ly_2 = results.pose_landmarks.landmark[11].x, results.pose_landmarks.landmark[11].y
        l_standard = math.hypot(lx_0 - lx_1, ly_0 - ly_1)
        l_length = math.hypot(lx_0 - lx_2, ly_0 - ly_2)

        if (l_length<l_standard or r_length<r_standard):
            if counter_flag==0:
                counter+=1
                counter_flag=1
        else:
            counter_flag=0

    cv2.putText(img, f'Times:{counter}', (20, 100), 1, cv2.FONT_HERSHEY_COMPLEX, (255, 0, 0), 2)

    ctime=time.time()
    fps=round(1/(ctime-ptime),1)
    ptime=ctime
    cv2.putText(img,f'FPS:{fps}',(20,50),1,cv2.FONT_HERSHEY_COMPLEX,(255,0,0),2)
    cv2.imshow('Push_up_counter', img)
    cv2.waitKey(1)
cap.release()