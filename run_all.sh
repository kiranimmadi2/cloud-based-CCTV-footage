#!/bin/bash
set -e

docker-compose up -d

until docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list >/dev/null 2>&1; do
  sleep 5
done
until curl -s http://localhost:19530 >/dev/null; do
  sleep 5
done

export RTSP_URL="rtsp://example/stream"
export CAM_ID="cam1"
python edge/stream.py "$RTSP_URL" "$CAM_ID" &
python ingest/consumer.py &
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
python tracker/reid.py --live &
uvicorn dashboard.app:app --host 0.0.0.0 --port 8080 &

echo "API http://localhost:8000" 
echo "Dashboard http://localhost:8080" 
wait
