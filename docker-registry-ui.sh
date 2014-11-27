#!/bin/bash
SERVICE_DIR=/db/docker-registry-ui
docker run \
-d \
-e $SERVICE_DIR \
-e SERVICE_ADDRESS=0.0.0.0 \
-e SERVICE_PORT=5000 \
-e GUNICORN_WORKERS=8 \
-p 5000:5000 \
-v ${SERVICE_DIR}:${SERVICE_DIR} \
arkii/gunicorn bash ${SERVICE_DIR}/start.sh