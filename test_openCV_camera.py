import cv2
import requests
import json
import datetime
import os
import RPi.GPIO as GPIO
import time

dt_now = datetime.datetime.now()

file_name = '%s.png' % dt_now.strftime("%Y-%m-%d %H:%M:%S")

WIDTH = 1280
HEIGHT = 960

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

ret, frame = cap.read()
print("撮影完了")
img = frame[270:830,220:1000]
cv2.imwrite(file_name, img)
cap.release()