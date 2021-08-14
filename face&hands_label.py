import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

#####################################################
#攝像頭大小設置
wCam,hCam=1280,920
#####################################################
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
hands=mp_hands.Hands()
face_mesh=mp_face_mesh.FaceMesh()
while cap.isOpened():
    success, image = cap.read()

    image_RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask=np.zeros(image.shape[:])
    results = face_mesh.process(image_RGB)

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=mask,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACE_CONNECTIONS,
            landmark_drawing_spec=drawing_spec,
            connection_drawing_spec=drawing_spec)

    results = hands.process(image_RGB)

    if results.multi_hand_landmarks:
       for hand_landmarks in results.multi_hand_landmarks:

          mp_drawing.draw_landmarks(
              mask, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)
    cv2.imshow('mask', mask)

    cv2.waitKey(5)




cap.release()