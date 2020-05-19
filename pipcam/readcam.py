#!/usr/bin/python3
# Programed by M.kawase
# 組込AI研究所
# ラズベリーパイPIカメラ
# 画像読み取り部

import time
import cv2
import sys

dev='/dev/video0'
winn='show cam'
cap = cv2.VideoCapture(dev)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

if not cap.isOpened():
    sys.exit()

while True:
    r, frm = cap.read()
    if r:
        ts=str(int(time.time()) % 10)
        cv2.imshow(winn, frm)
        cv2.imwrite('./tmp'+ts+'.jpg',frm)
        time.sleep(0.8)
        if (cv2.waitKey(1) & 0xff) == ord('q'):
            break
    else:
       break

cv2.destroyWindow(winn)

