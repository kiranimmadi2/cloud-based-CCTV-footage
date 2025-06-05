import sys
import json
import cv2
from ultralytics import YOLO
import insightface
from confluent_kafka import Producer

rtsp_url=sys.argv[1]
cam_id=sys.argv[2]

cap=cv2.VideoCapture(rtsp_url)
model=YOLO('yolov8n.pt')
arc=insightface.model_zoo.get_model('arcface_r100_v1')
arc.prepare(ctx_id=-1)
prod=Producer({'bootstrap.servers':'localhost:9092'})
b=[]

while True:
    ret,fr=cap.read()
    if not ret:break
    for r in model(fr)[0].boxes.xyxy.cpu().tolist():
        x1,y1,x2,y2=map(int,r)
        crop=fr[y1:y2,x1:x2]
        if crop.size==0:continue
        emb=arc.get_embedding(crop).tolist()
        b.append(emb)
        if len(b)==10:
            prod.produce('faces.raw',json.dumps({'cam_id':cam_id,'embeddings':b}).encode())
            prod.flush()
            b=[]
cap.release()
