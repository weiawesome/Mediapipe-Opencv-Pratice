from number_gesture import *
import time
import cv2
import random
import hand
import math
class Bubble_game():
    def __init__(self,wcam=1000, hcam = 1000,count_time=5,game_time=60,exist_time=10,bubble_num=5,bubble_radius=15):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, wcam)
        self.cap.set(4, hcam)
        self.ptime = time.time()
        self.game_start_time=time.time()
        self.img=[]
        self.detector = hand.handDector()
        self.bubble = []
        self.bubble_colors = []
        self.bubble_num=bubble_num
        self.bubble_radius=bubble_radius
        self.count_time=count_time
        self.Exist_time=exist_time
        self.Game_time=game_time
        self.score=0
        self.ranklist=['000','000','000']
    def fps(self,fps_color):
        ctime = time.time()
        fps = round(1 / (ctime - self.ptime), 1)
        self.ptime = ctime
        cv2.putText(self.img, f'FPS:{fps}', (20, 35), 2, cv2.FONT_HERSHEY_PLAIN, fps_color, 2)
    def time_period(self,ctime,root,color):
        if root[0]==False:
            ctime=time.time()
        else:
            if ((time.time()-ctime)<1):
                cv2.putText(self.img,'Ready:',root[1],2,cv2.FONT_HERSHEY_PLAIN,color,2)
            elif ((time.time() - ctime) > self.count_time+2):
                self.playing()
            else:
                cv2.putText(self.img,f'00:0{int(7-time.time()+ctime)}', root[1], 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        return ctime
    def bubble_time(self):
        if time.time() - self.generate_time > self.Exist_time:
            return True
        return False
    def game_time(self,color):
        t = int(self.Game_time+1 - time.time() + self.game_start_time)
        if (t<0):
            print("Game over!   Score:", self.score)
            self.reset_rank()
            self.start()
        mt,st=t//60,t%60
        if mt < 10:
            if st < 10:
                cv2.putText(self.img, f'Time:0{mt}:0{st}', (self.img.shape[0] - 20, 30), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
            else:
                cv2.putText(self.img, f'Time:0{mt}:{st}', (self.img.shape[0] - 20, 30), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        else:
            if st < 10:
                cv2.putText(self.img, f'Time:{mt}:0{st}', (self.img.shape[0] - 20, 30), 2, cv2.FONT_HERSHEY_PLAIN,color, 2)
            else:
                cv2.putText(self.img, f'Time:{mt}:{st}', (self.img.shape[0] - 20, 30), 2, cv2.FONT_HERSHEY_PLAIN, color,2)
    def rank_bar(self,color):
        cv2.putText(self.img,'Ranking', (self.img.shape[0] - 50, 40), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        cv2.putText(self.img, '  1 : '+self.ranklist[0], (self.img.shape[0] - 50, 75), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        cv2.putText(self.img, '  2 : '+self.ranklist[1], (self.img.shape[0] - 50, 110), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        cv2.putText(self.img, '  3 : '+self.ranklist[2], (self.img.shape[0] - 50, 145), 2, cv2.FONT_HERSHEY_PLAIN, color, 2)
        color=[color[1],color[2],color[0]]
        x, y,x1, y1=self.img.shape[0] - 70, 10,self.img.shape[0]+145, 155
        l = (x1-x) // 4 if (y1-y) > (x1-x) else (y1-y) // 4
        cv2.line(self.img, (x, y), (x + l, y), color, 5)
        cv2.line(self.img, (x, y), (x, y + l), color, 5)

        cv2.line(self.img, (x1, y), (x1 - l, y),color, 5)
        cv2.line(self.img, (x1, y), (x1, y + l),color, 5)

        cv2.line(self.img, (x, y1), (x + l, y1),color, 5)
        cv2.line(self.img, (x, y1), (x, y1 - l),color, 5)

        cv2.line(self.img, (x1, y1), (x1 - l, y1),color, 5)
        cv2.line(self.img, (x1, y1), (x1, y1 - l),color, 5)

        cv2.rectangle(self.img, (x,y),(x1,y1),color, 2)

    def rand_bubble(self):
        self.generate_time=time.time()
        self.bubble = []
        self.bubble_colors = []
        h, w, c = self.img.shape
        for i in range(self.bubble_num):
            self.bubble.append((random.randint(0 + 20, w - 20), random.randint(0 + 20, h - 20)))
            self.bubble_colors.append((random.randint(0, 256), random.randint(0, 256), random.randint(0, 256)))
    def paint_bubble(self):
        for i in range(len(self.bubble)):
            cv2.circle(self.img, self.bubble[i], self.bubble_radius, self.bubble_colors[i], self.bubble_radius//2)
    def kill_bubble(self,lm):
        min_x, max_x, min_y, max_y = lm[0][1], lm[0][1], lm[0][2], lm[0][2]
        for i in lm:
            min_x = min(min_x, i[1])
            min_y = min(min_y, i[2])
            max_x = max(max_x, i[1])
            max_y = max(max_y, i[2])
        cx,cy=(min_x+max_x)/2,(min_y+max_y)/2
        radius=math.hypot(cx-min_x,cy-min_y)
        del_ma=[]
        for i in range(len(self.bubble)):
            x, y = self.bubble[i]
            if math.hypot(x - cx, y - cy) < radius:
                del_ma.append(i)
        del_ma.reverse()
        self.score += 10 * len(del_ma)
        for i in del_ma:
            self.bubble.pop(i)
            self.bubble_colors.pop(i)
    def touch_bubble(self):
        lm1, lm2 =self.detector.findposition(self.img, draw=False)
        if lm1:
            self.kill_bubble(lm1)
        if lm2:
            self.kill_bubble(lm2)
    def Score(self):
        cv2.putText(self.img, f'Score:{self.score}', (20, 75), 3, cv2.FONT_HERSHEY_PLAIN, (0, 0, 255), 2)
    def reset_rank(self):
        str_score=''
        while(self.score!=0):
            str_score+=str(self.score%10)
            self.score=self.score//10
        if len(str_score)<3:
            str_score=str_score+('0'*(3-len(str_score)))
        str_score=str_score[::-1]
        for i in range(len(self.ranklist)):
            if int(str_score)>int(self.ranklist[i]):
                self.ranklist.insert(i,str_score)
                break
        self.ranklist.pop()

    def start(self):
        fps_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        time_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        bar_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        s_time = time.time()
        while True:
            sucess, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 1)
            self.rank_bar(bar_color)
            finger_Num = finger_number(self.img)
            s_time = self.time_period(s_time, finger_Num.ya_ges(), time_color)
            self.fps(fps_color)
            cv2.imshow('Game_bubble', self.img)
            cv2.waitKey(1)
    def playing(self):
        fps_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        time_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        self.game_start_time=time.time()
        self.score=0
        while True:
            sucess, self.img = self.cap.read()
            self.img = cv2.flip(self.img, 1)
            self.game_time(time_color)
            self.Score()
            if len(self.bubble) == 0 or self.bubble_time():
                self.rand_bubble()
            self.paint_bubble()
            self.touch_bubble()
            self.fps(fps_color)
            cv2.imshow('Game_bubble', self.img)
            cv2.waitKey(1)
def main():
    game=Bubble_game()
    game.start()
if __name__=='__main__':
    main()