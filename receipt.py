import cv2
import requests
import json
import datetime
import os
import RPi.GPIO as GPIO
import time

PNO = 2 #GPIOポート番号

GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO, GPIO.OUT)

TOKEN = "xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CHANNEL = "領収書"

# ボタンを押したらプログラムを呼び出す
if __name__ == "__main__":
    # GPIOピン番号設定
    pin1 =  23

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    # ボタンクリック待機中
    print("ボタン待機中...")

    while True:
        button1 = GPIO.input(pin1)

        cmd = ""
        if button1 == 1:
            print("ボタンが押されました")
            
            GPIO.output(PNO, GPIO.HIGH) # 点灯
            time.sleep(0.4)
            GPIO.output(PNO, GPIO.LOW) # 消灯
            time.sleep(0.4)
            # ボタン1の処理
            cmd = "sudo python3 /home/pi/receipt.py"

        # 実行
        if cmd != "":
            dt_now = datetime.datetime.now()
            file_name = '%s.png' % dt_now.strftime("%Y-%m-%d %H:%M:%S")
            
            #ret = os.popen(cmd).readline().strip()
            #print(ret)
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
            
            ret, frame = cap.read()
            print("撮影完了")
            img = frame[270:830,220:1000]
            print("トリミング")
            cv2.imwrite(file_name, img)

            files = {'file': open('./'+file_name, 'rb')}
            param = {
                        'token':TOKEN, 
                        'channels':[CHANNEL],
                        'initial_comment': dt_now.strftime('%Y年%m月%d日 %H:%M:%S'),
            }
            r = requests.post(url="https://slack.com/api/files.upload", data=param, files=files)
            print(r.json())
            
            os.remove('./'+file_name)
            cap.release()

            for i in range(5):
                GPIO.output(PNO, GPIO.HIGH) # 点灯
                time.sleep(0.4)
                GPIO.output(PNO, GPIO.LOW) # 消灯
                time.sleep(0.4)
                
            time.sleep(1) # ボタンを押した後のチャタリング防止のため

        time.sleep(0.1)

GPIO.cleanup()