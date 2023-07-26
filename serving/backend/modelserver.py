from fastapi import FastAPI, File, UploadFile

import uvicorn
import torch
import cv2
import json
import time
import albumentations as A
import numpy as np
import torch.nn.functional as F

#모델 출력을 dict로 만드는 함수
def output2dict(output):
    class_threshold = 0
    allergy_threshold = 0.5
    
    arr1 = [(score, index) for index, score in enumerate(output[:93])]
    arr1.sort(reverse=True)
    result = []
    for i in range(3):
        score = arr1[i][0]
        index = arr1[i][1]
        dish = classes[str(index)]
        if score > class_threshold:
            valid = True
        else:
            valid = False
        dictionary = {'class' : dish, 'recipe' : recipes[dish], 'valid' : valid}
        result.append(dictionary)

    arr2 = [(score, index) for index, score in enumerate(output[93:])]
    arr2.sort(reverse=True)
    for (score, index) in arr2:
        if score > allergy_threshold:
            for i in range(len(result)):
                result[i]['recipe'].append(allergy[str(index)])

    for i in range(len(result)):
        result[i]['recipe'] = list(set(result[i]['recipe']))

    result = {'result' : result}

    return result

app = FastAPI()

@app.post('/upload')
async def upload(file: dict):
    global num
    num = num + 1
    
    with open('./data/' + str(num) + '.jpg', 'wb') as f:
        image = np.array(file['image'], dtype=np.uint8).tobytes()
        f.write(image)

    image = cv2.imread('./data/' + str(num) + '.jpg', cv2.IMREAD_COLOR)

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
    output = F.sigmoid(output[0])
    result = output2dict(output)

    print(result, type(result))

    return result

if __name__ == '__main__':
    model = torch.load('./pthfile/Tresnet_m_ml_decoder_recipy_final_latest.pth').cuda()
    model.eval()
    with open('./order/order.json') as file:
        classes = json.load(file)
    with open('./DB/DB.json') as file:
        recipes = json.load(file)
    with open('./allergy/allergy.json') as file:
        allergy = json.load(file)
    global num
    num = 0

    uvicorn.run(app, host='', port=30009)