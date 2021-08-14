import cv2
import os
import time
import hand as hmt
import random
#####################################################
#分辨手指數字物件
class finger_number():
    def __init__(self,img,hand_tip=[4,8,12,16,20],folderPath='Gesture',detector=hmt.handDector(dectionCon=0.75)):
        self.hand_tip=hand_tip
        self.overlayList=[]
        myList = os.listdir(folderPath)
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            self.overlayList.append(image)
        self.detector=detector
        self.img=img
        self.finger_flag=[0] * len(self.hand_tip)
        # self.finger_capture()

    #####################################################
    #手指處理
    def finger_process(self,landmark):
        for tip in self.hand_tip:
            #####################################################
            #處理其它手指
            if landmark[tip][2] < landmark[tip - 3][2]:
                self.finger_flag[self.hand_tip.index(tip)] = 1
            else:
                self.finger_flag[self.hand_tip.index(tip)] = 0
            #####################################################

            #####################################################
            #處理大拇指
            if tip == 4:
                #大拇指在右側
                if landmark[5][1] < landmark[9][1]:
                    if landmark[tip][1] < landmark[tip - 1][1]:
                        self.finger_flag[self.hand_tip.index(tip)] = 1
                    else:
                        self.finger_flag[self.hand_tip.index(tip)] = 0
                #大拇指在左側
                else:
                    if landmark[tip][1] > landmark[tip - 1][1]:
                        self.finger_flag[self.hand_tip.index(tip)] = 1
                    else:
                        self.finger_flag[self.hand_tip.index(tip)] = 0
            #####################################################
    #####################################################

    #####################################################
    #對伸出的手指數量分類
    def finger_num(self):
        num=None
        if self.finger_flag==[0,0,0,0,0]:
            num=0
        elif self.finger_flag==[0,1,0,0,0]:
            num=1
        elif self.finger_flag==[0,1,1,0,0]:
            num=2
        elif self.finger_flag==[0,1,1,1,0]:
            num=3
        elif self.finger_flag==[0,1,1,1,1]:
            num=4
        elif self.finger_flag==[1,1,1,1,1]:
            num=5
        elif self.finger_flag==[1,0,0,0,1] or self.finger_flag==[1,0,0,0,0]:
            num=6
        elif self.finger_flag==[1,1,0,0,0]:
            num=7
        elif self.finger_flag==[1,1,1,0,0]:
            num=8
        elif self.finger_flag==[1,1,1,1,0]:
            num=9
        return num
    #####################################################

    #####################################################
    #對應手指的數字及圖的位置
    def finger_capture(self):
        self.img = self.detector.findhands(self.img)
        landmark_0, landmark_1 = self.detector.findposition(self.img, draw=False)

        if len(landmark_0) != 0:
            self.finger_process(landmark_0)
            num_0 = self.finger_num()
            if len(landmark_1) == 0 and num_0!=None:
                h, w, c = self.overlayList[num_0].shape
                self.img[0:h, 0:w] = self.overlayList[num_0]
        if len(landmark_1) != 0:
            self.finger_process(landmark_1)
            num_1 = self.finger_num()
            if landmark_0[4][1] > landmark_1[4][1]:
                num_0, num_1 = num_1, num_0
            if num_1!=None and num_0!=None:
                h, w, c = self.overlayList[num_1].shape
                self.img[0:h, 0:w] = self.overlayList[num_0]
                self.img[0:h, (640 - w):640] = self.overlayList[num_1]
            elif num_0!=None:
                h, w, c = self.overlayList[num_0].shape
                self.img[0:h, 0:w] = self.overlayList[num_0]
            elif num_1!=None:
                h, w, c = self.overlayList[num_1].shape
                self.img[0:h, (640 - w):640] = self.overlayList[num_1]
    def draw_ya_box(self,landmark,color,t):
        x, x1, y, y1 = landmark[0][1], landmark[0][1], landmark[0][2], landmark[0][2]
        for i in landmark:
            x = min(x, i[1])
            y = min(y, i[2])
            x1 = max(x1, i[1])
            y1 = max(y1, i[2])
        x -= 20
        y -= 20
        x1 += 20
        y1 += 20
        w, h = x1 - x, y1 - y
        l = w // 4 if h > w else h // 4
        cv2.line(self.img, (x, y), (x + l, y), color, t)
        cv2.line(self.img, (x, y), (x, y + l), color, t)

        cv2.line(self.img, (x1, y), (x1 - l, y), color, t)
        cv2.line(self.img, (x1, y), (x1, y + l), color, t)

        cv2.line(self.img, (x, y1), (x + l, y1), color, t)
        cv2.line(self.img, (x, y1), (x, y1 - l), color, t)

        cv2.line(self.img, (x1, y1), (x1 - l, y1), color, t)
        cv2.line(self.img, (x1, y1), (x1, y1 - l), color, t)

        cv2.rectangle(self.img, (x, y),(x1, y1), color, 1)

        return (x,y-5)

    def ya_ges(self):
        self.img = self.detector.findhands(self.img,draw=False)
        landmark_0, landmark_1 = self.detector.findposition(self.img, draw=False)

        if len(landmark_0) != 0:
            self.finger_process(landmark_0)
            num = self.finger_num()
            if num==2:
                color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                return True,self.draw_ya_box(landmark_0,color,5)
            elif len(landmark_1)!=0:
                self.finger_process(landmark_1)
                num = self.finger_num()
                if num==2:
                    color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                    return True,self.draw_ya_box(landmark_1, color, 5)
        return False,[]


    #####################################################
#####################################################

def main():

    #####################################################
    #攝像頭設置
    wcam,hcam=640,480
    cap=cv2.VideoCapture(0)
    cap.set(3,wcam)
    cap.set(4,hcam)
    ctime=0
    ptime=0
    #####################################################

    while cap.isOpened():
        sucess,img=cap.read()
        img=cv2.flip(img,1)
        finger_Num=finger_number(img)
        print(finger_Num.ya_ges())
        img=finger_Num.img
        ctime=time.time()
        fps=round(1/(ctime-ptime),1)
        ptime=ctime
        cv2.putText(img,f'FPS:{fps}',(30,120),2,cv2.FONT_HERSHEY_PLAIN,(255,0,255),2)
        cv2.imshow('Finger_Number',img)
        cv2.waitKey(1)
if __name__=='__main__':
    main()
