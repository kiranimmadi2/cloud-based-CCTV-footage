import cv2,io,os
import numpy as np
import insightface
from fastapi import FastAPI,UploadFile,File
from .milvus import search

arc=insightface.model_zoo.get_model('arcface_r100_v1')
arc.prepare(ctx_id=-1)
app=FastAPI()

@app.post('/search')
async def do_search(img:UploadFile=File(...),k:int=5):
    buf=await img.read()
    arr=np.frombuffer(buf,np.uint8)
    im=cv2.imdecode(arr,cv2.IMREAD_COLOR)
    emb=arc.get_embedding(im).tolist()
    res=search(emb,k)
    return res

@app.get('/health')
async def health():
    return {'status':'ok'}
