import os, cv2, json, argparse
from ultralytics import YOLO
import insightface
from confluent_kafka import Producer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('rtsp_url')
    ap.add_argument('cam_id')
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.rtsp_url)
    det = YOLO('yolov8n-face.pt')
    rec = insightface.model_zoo.get_model('buffalo_l', download=True)
    rec.prepare(ctx_id=-1)
    prod = Producer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')})
    buf = []
    while True:
        ok, img = cap.read()
        if not ok:
            break
        res = det(img)[0]
        if res.boxes is None:
            continue
        for box in res.boxes.xyxy.cpu().numpy().astype(int):
            x1, y1, x2, y2 = box
            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue
            crop = cv2.resize(crop, rec.input_size)
            emb = rec.get_feat(crop)[0].tolist()
            buf.append({'cam_id': a.cam_id, 'vec': emb})
            if len(buf) == 10:
                prod.produce('faces.raw', json.dumps(buf).encode())
                prod.flush()
                buf.clear()


if __name__ == '__main__':
    main()
