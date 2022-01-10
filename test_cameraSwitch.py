# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys, os

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
            # ボタン1の処理
            cmd = "sudo python3 /home/pi/receipt.py"

        # 実行
        if cmd != "":
            ret = os.popen(cmd).readline().strip()
            print(ret)
            time.sleep(1) # ボタンを押した後のチャタリング防止のため

        time.sleep(0.1)

    GPIO.cleanup()