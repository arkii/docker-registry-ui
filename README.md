docker-registry-ui
==================

v0.01

##Installation

```Bash
git clone https://github.com/ARKII/docker-registry-ui.git
cd docker-registry-ui
sudo pip install -r requirements.txt
vi configuration.py
sudo python ./docker-registry-ui.py
```

Visit http://ip:5000/


## Screenshot
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/1.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/2.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/3.png)
![image](https://github.com/ARKII/docker-registry-ui/blob/master/test/4.png)







##
Read

https://docs.docker.com/reference/api/registry_api/


http://10.15.184.241:5000/v1/_ping
true
http://10.15.184.241:5000/v1/search?q=arkii
{"num_results": 1, "query": "arkii", "results": [{"description": null, "name": "arkii/centos65-httpd-2.0.65"}]}
https://docs.docker.com/reference/api/docker-io_api/
https://docs.docker.com/reference/api/registry_api/


#删除tag
curl -X DELETE 10.15.184.241/v1/repositories/library/centos/tags/centos5
#删除repo
curl -X DELETE 10.15.184.241/v1/repositories/library/centos7/
