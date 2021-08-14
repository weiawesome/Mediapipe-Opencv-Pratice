import cv2
import mediapipe as mp
import time
import random

class Face_Detection():
    def __init__(self,conf=0.75,t=5,rt=1):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(conf)
        self.color=(0,0,0)
        self.t = t
        self.rt = rt
    def fancy_draw(self,img, bbox,id):
        random.seed(id)
        l=bbox[2]//4 if bbox[3]>bbox[2] else bbox[3]//4
        self.color=(random.randint(0,256),random.randint(0,256),random.randint(0,256))
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cv2.line(img, (x, y), (x + l, y), self.color, self.t)
        cv2.line(img, (x, y), (x, y + l), self.color, self.t)

        cv2.line(img, (x1, y), (x1 - l, y), self.color, self.t)
        cv2.line(img, (x1, y), (x1, y + l), self.color, self.t)

        cv2.line(img, (x, y1), (x + l, y1), self.color, self.t)
        cv2.line(img, (x, y1), (x, y1 - l), self.color, self.t)

        cv2.line(img, (x1, y1), (x1 - l, y1), self.color, self.t)
        cv2.line(img, (x1, y1), (x1, y1 - l), self.color, self.t)

        cv2.rectangle(img, bbox, self.color, self.rt)

        return img

    def detect(self,img,get_accuracy=True):
        ALL_boxes=[]
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceDetection.process(imgRGB)
        if results.detections:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                ALL_boxes.append((detection.score[0], (bbox)))
                img=self.fancy_draw(img, bbox,id)
                if get_accuracy:
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,2, self.color, 2)
        return img,ALL_boxes




def main():
    cap=cv2.VideoCapture(0)
    ptime=0
    d=Face_Detection()
    while True:
        sucess,img=cap.read()
        img,boxes=d.detect(img)
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)
        cv2.imshow('img',img)
        if cv2.waitKey(1)==('8'):
            break


if __name__=='__main__':
    main()