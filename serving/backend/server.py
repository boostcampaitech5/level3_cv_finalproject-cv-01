from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import uvicorn
import requests
import threading

app = FastAPI()

@app.post('/upload')
async def upload(file: dict):#UploadFile or bytes
    url = 'http://101.101.208.43:30009/upload'

    lockindex = -1
    while True:
        for index, L in enumerate(lock):
            if L.acquire(timeout=0.01):
                lockindex = index
                break
        if lockindex > -1:
            break
        else:
            print('blocked')
    
    response = requests.post(url, json=file)

    lock[lockindex].release()
    
    return JSONResponse(content=jsonable_encoder(response.json()), status_code=200)

if __name__ == '__main__':
    lock = []
    lock.append(threading.Lock())
    uvicorn.run(app, host='', port=30010)