docker-registry-ui
==================

v0.02

##Installation

###The normal way
```Bash
git clone https://github.com/ARKII/docker-registry-ui.git
cd docker-registry-ui
sudo pip install -r requirements.txt
vi configuration.py
sudo python ./docker-registry-ui.py
```

###The docker way
```Bash
git clone https://github.com/ARKII/docker-registry-ui.git
cd docker-registry-ui
vi configuration.py
sh docker-registry-ui.sh
or

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

```


Visit http://ip:5000/


##Screenshot
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/1.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/2.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/3.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/4.png)







##Read

https://docs.docker.com/reference/api/registry_api/

```
curl http://10.15.184.241:5000/v1/_ping
```
true
```
curl http://10.15.184.241:5000/v1/search?q=arkii
```
{"num_results": 1, "query": "arkii", "results": [{"description": null, "name": "arkii/centos65-httpd-2.0.65"}]}



删除tag
```
curl -X DELETE 10.15.184.241/v1/repositories/library/centos/tags/centos5
```
删除repo
```
curl -X DELETE 10.15.184.241/v1/repositories/library/centos7/
```