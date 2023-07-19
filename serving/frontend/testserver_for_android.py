from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
app = FastAPI()

import numpy as np
@app.post('/upload')
def dd(data:dict):
    print(type(data['image']))
    with open("./img.jpg",'wb') as f:
        np_arr = np.array(data['image'], dtype=np.uint8)
        f.write(np_arr.tobytes())
    return JSONResponse(content=jsonable_encoder({"result":[{"class":"baek_sook", "recipes":["egg","beef","pork"]},
                                                            {"class":"BBQ", "recipes":["egg","beef","pork"]},
                                                            {"class":"beef_tartare", "recipes":["egg","beef","pork"]}]}),status_code=200)

@app.get('/test')
def test():
    print('ss')
    return JSONResponse(content='success',status_code=200)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0,0,0,0",port=30012)