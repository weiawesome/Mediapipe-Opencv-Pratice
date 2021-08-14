import cv2
import time
import mediapipe as mp

class handDector():
    def __init__(self,mode=False,maxHands=2,dectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.dectionCon=dectionCon
        self.trackCon=trackCon


        self.mp_hands = mp.solutions.hands
        self.hands=self.mp_hands.Hands(self.mode,self.maxHands,self.dectionCon,self.trackCon)
        self.mpdraw=mp.solutions.drawing_utils
    def findhands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRGB)
        #print(self.result.multi_hand_landmarks)
        if (self.result.multi_hand_landmarks):
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlms,self.mp_hands.HAND_CONNECTIONS)
        return img
    def findposition(self,img,handNum_0=0,handNum_1=1,draw=True):
        lmList_0=[]
        lmList_1=[]
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        try:
            self.result.multi_hand_landmarks[handNum_0],self.result.multi_hand_landmarks[handNum_1]=self.result.multi_hand_landmarks[handNum_1],self.result.multi_hand_landmarks[handNum_0]
            if (self.result.multi_hand_landmarks):
                myHand = self.result.multi_hand_landmarks[handNum_1]
                for id, lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id,cx,cy)
                    lmList_1.append([id, cx, cy])
                    # if id==0:
                    if draw:
                        cv2.circle(img, (cx, cy), 7, (255, 0,0), cv2.FILLED)
        except:
            pass
        if (self.result.multi_hand_landmarks):
            myHand=self.result.multi_hand_landmarks[handNum_0]
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmList_0.append([id,cx,cy])
                #if id==0:
                if draw:
                    cv2.circle(img,(cx,cy),7,(255,0,255),cv2.FILLED)

        return lmList_0,lmList_1
def main():
    cap = cv2.VideoCapture(0)
    ptime = 0
    ctime = 0
    detector=handDector()
    while True:
        sucess, img = cap.read()
        img=detector.findhands(img)
        lmList_0,lmList_1=detector.findposition(img)
        if len(lmList_0)!=0:
            print(lmList_0[4])
        if len(lmList_1)!=0:
            print(lmList_1[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow('img', img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()
