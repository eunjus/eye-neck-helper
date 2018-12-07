# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 23:18:00 2018

@author: 배보은
"""

import cv2
import datetime
import ctypes
import serial


def motor():
    ser = serial.Serial("COM3", 9600) 

    motor_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    while True:
        
        ret_val, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        m = motor_cascade.detectMultiScale(gray, 1.3, 5)
        
        left1="top up"
        left2="top down"
        center="stop"
        right1="bottom up"
        right2="bottom down"
        
        for (x,y,w,h) in m:
            a=x+int(w/2)
            b=y+int(h/2)
            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)      
            cv2.line(img,(130,0),(130,500),(188,166,244),2)
            cv2.line(img,(260,0),(260,500),(188,166,244),2)
            cv2.line(img,(390,0),(390,500),(188,166,244),2)
            cv2.line(img,(520,0),(520,500),(188,166,244),2)
            cv2.circle(img,(a,b),2,(0,0,255),-1)
        if True: 
            img = cv2.flip(img, 1)
            
        
        for (x,y,w,h) in m:
            cv2.putText(img,left1,(420,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
            cv2.putText(img,left2,(540,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
            cv2.putText(img,center,(300,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
            cv2.putText(img,right1,(140,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
            cv2.putText(img,right2,(5,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
     
       
        cv2.imshow('my webcam', img)
        print('좌표값: ', x,y )
        
        if 300<x<420:
            print("하단모터올리기",1)
            ser.write(b'1')
            ser.send_break(0.25) #시리얼통신 시 데이터충돌방지를 위해 딜레이 시켜줌
        elif 430<a<650:
            print("하단모터내리기",2)
            ser.write(b'2')
            ser.send_break(0.25)
        elif 30<x<150:
            print("상단모터올리기",3)
            ser.write(b'3')
            ser.send_break(0.25)
        elif 0<x<25:
            print("상단모터내리기",4)
            ser.write(b'4')
            ser.send_break(0.25)
        elif 160<x<270:
            print("작동멈춤",5)
            ser.write(b'5')
            ser.send_break(0.25)
        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()

    
def blink():    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascase-eye.xml')
    
    cap = cv2.VideoCapture(0)

    global c

    c=1 # 맨 처음 눈을 깜빡였을 때 값을 1로 내보내 주기 위한 초기값 설정
    start_date = datetime.datetime.utcnow()
    
    while (datetime.datetime.utcnow() - start_date).seconds < 10: # 10초 간격으로 눈 깜빡임 인식
        
        
        ret, img = cap.read()
        if True:
            img = cv2.flip(img, 1)
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) # 얼굴 값 받아옴
    
        for (x,y,w,h) in faces: # 얼굴만 인식 및 눈 값 받아옴 k = 1
            k=1
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
    
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:# 눈을 깜빡이지 않았을 때(사라지지 않았을 때) k = 0 이 됨
                k=0
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
            if(k==1): # 눈이 사라지고 얼굴만 인식 되었을 때 (k = 1)
                t="Blinked!",c
                c=c+1
                print(t)            
                    
            else: # 눈을 깜빡이지 않았을 때 k = 0
                print("Not blinking")
    
    
        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # ESC 키를 눌렀을 때 얼굴과 눈 인식을 멈춘다. 
            break # 가장 가까운 while문을 빠져나간다. 
    
    cap.release()
    cv2.destroyAllWindows()
    return c

    
    
def check(x): # 설정한 시간동안의 c값(눈 깜빡인 횟수)을 확인하여 팝업창을 띄어주는 함수
    global msg

    print(x-1)
    if x<10: # 10초안에 10번 이하로 깜빡이면 팝업창 띄움. 
        msg=ctypes.windll.user32.MessageBoxW(None,"눈이 건조합니다. 1분동안 10회 이하로 깜박였습니다. 계속 실행하시겠습니까? ","경고창",4)
        if msg==6: #예 버튼 눌렀을때
            blink()
        elif msg==7: #아니오 버튼 눌렀을 때 프로그램 종료
              quit()         
    else:
        blink()
        


start=ctypes.windll.user32.MessageBoxW(None,"EYE HELPER를 실행하시겠습니까? 아니오를 누르면 NECK HELPER로 이동","EYE NECK HELPER",4)
if start == 6:
     blink()
     while True:
         check(c)
         if msg == 7:
             break
elif start==7:
     motor()
     
    

        





