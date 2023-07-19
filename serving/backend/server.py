from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.templating import Jinja2Templates

import uvicorn
import torch
import cv2
import json
import requests
import threading
import albumentations as A
import numpy as np
import torch.nn.functional as F

app = FastAPI()

@app.post('/upload')
async def upload(file: bytes = File(...)):#UploadFile(파일을 받지 않고 코드를 진행하는 거 같다.) or bytes(파일을 다 받고 코드를 진행하는 거 같다.)
    url = 'http://101.101.208.43:30009/upload'
    
    files = {'file' : file}

    #Lock을 획득한다.
    lockindex = -1
    while True:
        for index, L in enumerate(lock):
            if L.acquire(timeout=0.1):
                lockindex = index
                break
        if lockindex > -1:
            break
        else:
            print('blocked')
    
    response = requests.post(url, files=files)

    lock[lockindex].release()

    return response.json()

if __name__ == '__main__':
    #Lock을 획득한 스레드는 모델 서버에 파일을 전송한다.
    lock = []
    lock.append(threading.Lock())

    uvicorn.run(app, host='', port=30010)