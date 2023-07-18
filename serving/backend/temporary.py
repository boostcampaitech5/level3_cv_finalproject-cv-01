from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import uvicorn
import torch
import cv2
import json
import albumentations as A
import numpy as np
import torch.nn.functional as F

def output2dict(output):
    THRESHOLD = 0.5
    arr = [(score, index) for index, score in enumerate(output)]
    arr.sort()
    arr.reverse()
    result = []
    for i in range(3):
        score = arr[i][0]
        index = arr[i][1]
        dish = classes[str(index)]
        if score > THRESHOLD:
            valid = True
        else:
            valid = False
        dictionary = {'class' : dish, 'recipe' : recipes[dish], 'valid' : valid}
        result.append(dictionary)
    return {'result' : result}

app = FastAPI()

@app.post('/upload')
async def upload(file: dict):
    with open('/opt/ml/fastapi/data/test.jpg', 'wb') as f:
        image = np.array(file['image'], dtype=np.uint8)
        f.write(image.tobytes())

    image = cv2.imread('/opt/ml/fastapi/data/test.jpg', cv2.IMREAD_COLOR)

    print(image.shape)

    #transforms
    width = image.shape[0]
    height = image.shape[1]
    worh = min(width, height)
    transforms = A.Compose([
        A.CenterCrop(worh, worh),
        A.Resize(224, 224),
        A.Normalize()
    ])
    tem = {'image' : image}
    transformed = transforms(**tem)
    image = transformed['image']#(224, 224, 3)
    
    #(224, 224, 3) to (1, 3, 224, 224)
    image = np.transpose(image, (2, 0, 1))
    image = np.expand_dims(image, axis=0)

    image = torch.tensor(image).cuda()

    #inference
    output = model(image)
    output = F.softmax(output[0], dim=0)
    result = output2dict(output)
    
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

if __name__ == '__main__':
    model = torch.load('/opt/ml/fastapi/pthfile/ResNet18_best.pth').cuda()
    model.eval()
    with open('/opt/ml/fastapi/order/order.json') as file:
        classes = json.load(file)
    with open('/opt/ml/fastapi/DB/DB.json') as file:
        recipes = json.load(file)
    print('ready')

    uvicorn.run(app, host='', port=30009)