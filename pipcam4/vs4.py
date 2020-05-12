#!/usr/bin/python3
# programed by M.kawase
# 組込AI研究所(Embed AI Labo)
# ラズペリーパイIPカメラ
# Motion jpeg stream

import time
import cv2
from flask import Flask as fl, render_template as rt,Response

#ファイル書込みタイミング(秒)
wt=0.2
#何枚前の画像を転送するか？
bt=3

app=fl(__name__)

def getStream():
    while True:
        ts=str(int(time.time()/wt-bt) % 10)
        i=cv2.imread('./tmp'+ts+'.jpg')
        flg, frame = cv2.imencode('.jpg', i)
        yield b'--frame\r\n'+b'Content-Type: image/jpeg\r\n\r\n'+bytearray(frame)+b'\r\n\r\n'
        time.sleep(wt/2)

@app.route('/')
def main( ):
    return rt('index.html')

@app.route('/vs')
def stream( ):
    return Response(getStream(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
