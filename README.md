# ClearVision

ClearVision is a minimal demo for city-wide face search using streaming video. It leverages Kafka and Milvus for ingest and search, and exposes a simple dashboard.

## Services
- **edge** captures RTSP streams, performs face detection and embedding, and sends batches to Kafka.
- **ingest** reads detections from Kafka and stores embeddings with metadata in Milvus.
- **api** provides a REST search endpoint backed by Milvus.
- **tracker** links detections into tracks based on time and distance.
- **dashboard** shows search and tracking results on a map using WebSockets.

## Quick start
Run `./run_all.sh` to start local services with Docker and launch all components. After startup:
- API available at http://localhost:8000
- Dashboard at http://localhost:8080

This project uses minimal configuration and default camera locations. Update `cams` dictionaries in the Python code to reflect real coordinates.
