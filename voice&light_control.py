import cv2
import hand as htm
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import wmi
from PIL import ImageGrab

#####################################################
#攝像頭大小設置
wCam,hCam=640,480
#####################################################

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ctime=0
ptime=0

#####################################################
#亮度控制
WMI = wmi.WMI(namespace='root\WMI')
Light = WMI.WmiMonitorBrightnessMethods()[0]
light=0
lightBar=400
#####################################################

#####################################################
#音量控制
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
minvol=volRange[0]
maxvol=volRange[1]
vol=0
volBar=400
volper=0
detector=htm.handDector(dectionCon=0.7)
#####################################################

while True:
    sucess,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findhands(img)
    lmlist_0,lmlist_1=detector.findposition(img,draw=True)

    #####################################################
    #數據處理
    def lmlist_process(lmlist,img):
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
        length = math.hypot(x2 - x1, y2 - y1)
        if (length<50):
            cv2.circle(img, (cx, cy), 10, (0, 255,0), cv2.FILLED)
        return length
    #####################################################

    #####################################################
    #檢測第一隻手並控制音量
    if (len(lmlist_0)!=0):
        length_v = lmlist_process(lmlist_0, img)
        vol=np.interp(length_v,[70,250],[minvol,maxvol])
        volBar=np.interp(length_v,[70,200],[400,150])
        volper=np.interp(length_v,[70,200],[0,100])

        volume.SetMasterVolumeLevel(vol, None)
    #####################################################

    #####################################################
    #檢測第二隻手並控制亮度
    if (len(lmlist_1) != 0):
        length_l = lmlist_process(lmlist_1, img)
        light = np.interp(length_l, [70, 200], [0, 100])
        lightBar = np.interp(length_l, [70, 200], [400, 150])

        Light.WmiSetBrightness(Brightness=light, Timeout=5)
    #####################################################

    #####################################################
    #繪製音量控制條
    cv2.rectangle(img,(50,150),(85,400),(255,0,255),3)
    cv2.rectangle(img, (50,int(volBar)), (85, 400), (255,0, 255), cv2.FILLED)
    cv2.putText(img, f'{int(volper)}%', (30, 130), cv2.FAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION, 2, (255, 0, 255), 2)
    cv2.putText(img, 'Volume:', (20, 80), cv2.FAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION, 2, (255, 0, 255), 2)
    #####################################################

    #####################################################
    #繪製亮度控制條
    cv2.rectangle(img, (545, 150), (580, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (545, int(lightBar)), (580, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(light)}%', (520, 130), cv2.FAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION, 2, (255, 0, 0), 2)
    cv2.putText(img, 'Light:', (520, 80), cv2.FAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION, 2, (255, 0, 0), 2)
    #####################################################

    #####################################################
    #計算並繪製FPS
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f'FPS:{int(fps)}',(30,40),cv2.FAST_FEATURE_DETECTOR_NONMAX_SUPPRESSION,3,(0,255,0),2)
    #####################################################

    cv2.imshow('result',img)
    if cv2.waitKey(5)==ord('8'):
        break
cap.release()