#!/usr/bin/python3
# Programed By M.kawase
# 組込AI研究所(Embed AI Labo.)
# 

import glob
import time
import datetime as dt
import numpy as np
import cv2
from flask import Flask as fl, render_template as rt,Response

imgfiles=sorted(glob.glob('./images/*'))
imgmax=len(imgfiles)
sx = 200
sy = 200
pi = 3.1415
co = (0,255,0)

def writeclock(img):
    global sx,sy,pi,co
    cx, cy = (int(sx/2), int(sy/2))
    t = dt.datetime.now()
    # second
    sec = t.second
    secx = int((-cx+10) * np.sin(pi*(sec+30)/30) + cx)
    secy = int((cy-10) * np.cos(pi*(sec+30)/30) + cy)
    # minute
    min = t.minute
    minx = int((-cx+20) * np.sin(pi*(min+30)/30) + cx)
    miny = int((cy-20) * np.cos(pi*(min+30)/30) + cy)
    # hour
    hor = t.hour
    horx = int((-cx+40) * np.sin(pi*(hor+6)/6) + cx)
    hory = int((cy-40) * np.cos(pi*(hor+6)/6) + cy)
    cv2.line(img,(cx,cy),(secx,secy),co,2)
    cv2.line(img,(cx,cy),(minx,miny),co,4)
    cv2.line(img,(cx,cy),(horx,hory),co,4)

app=fl(__name__)

def getStream():
    global sx, sy
    n=0
    while True:
        if imgmax==0:
            i=np.zeros((sx, sy, 3), np.uint8)
        else:
            n = (n + 1) % imgmax
            i=cv2.imread(imgfiles[n])
            i=cv2.resize(i,(sx,sy))
        # strtm=str(dt.datetime.now())[11:19]
        # cv2.putText(i,strtm,(int(sx/10),int(sy/2)),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,0))
        writeclock(i)
        flg, frame = cv2.imencode('.jpg', i)
        yield b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n'+bytearray(frame)+b'\r\n\r\n'
        time.sleep(0.8)

@app.route('/')
def main( ):
    return rt('index.html')

@app.route('/clockimg')
def stream( ):
    return Response(getStream(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
