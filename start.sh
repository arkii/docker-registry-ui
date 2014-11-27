#/bin/bash
/usr/bin/gunicorn --chdir ${SERVICE_DIR:=/db/docker-registry-ui} \
--error-logfile ${SERVICE_DIR:=/db/docker-registry-ui}/log/registry-ui.log \
--access-logfile ${SERVICE_DIR:=/db/docker-registry-ui}/log/access.log \
--max-requests 100 --graceful-timeout 3600 -t 3600 -k gevent \
-b ${SERVICE_ADDRESS:=0.0.0.0}:${SERVICE_PORT:=5000} -w ${GUNICORN_WORKERS:=4} \
docker-registry-ui:app