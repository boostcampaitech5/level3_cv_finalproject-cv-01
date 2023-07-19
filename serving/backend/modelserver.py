from fastapi import FastAPI, Form, Request, File, UploadFile
from fastapi.templating import Jinja2Templates

import uvicorn
import torch
import cv2
import json
import albumentations as A
import numpy as np
import torch.nn.functional as F

#모델 출력을 dict로 만드는 함수
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
    return result

app = FastAPI()
templates = Jinja2Templates(directory='./')

@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    global num
    num = num + 1
    
    with open('/opt/ml/fastapi/data/' + str(num) + '.jpg', 'wb') as f:
        content = await file.read()
        f.write(content)

    image = cv2.imread('/opt/ml/fastapi/data/' + str(num) + '.jpg', cv2.IMREAD_COLOR)

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

    return result

if __name__ == '__main__':
    model = torch.load('/opt/ml/fastapi/pthfile/ResNet18_best.pth').cuda()
    model.eval()

    with open('/opt/ml/fastapi/order/order.json') as file:
        classes = json.load(file)

    with open('/opt/ml/fastapi/DB/DB.json') as file:
        recipes = json.load(file)

    #파일 이름에 사용할 변수
    global num
    num = 0

    uvicorn.run(app, host='', port=30009)