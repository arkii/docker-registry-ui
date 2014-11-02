# -*- coding: utf-8 -*-
__author__ = 'arkii'
__email__ = 'sun.qingyun@zol.com.cn'
__create__ = '10/30/14 19:48'


'''
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

'''



import json
import tarfile
import re
import os
from datetime import datetime

#from urllib2.parse import urlencode

from httplib import HTTPConnection

HTTP_HEADER = {
    "Cache-Control": "no-cache",
    "User-Agent": "DockerRegistryUI",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}

server = '10.15.184.241'
target = '/v1/_ping'
def registry_conn(ipaddr, uri):
    _uri = uri
    #_params = urlencode({'username': 'lb_fresh', 'password': 'ct557k3O6', 'url': _url, 'type': 1})
    _conn = HTTPConnection(ipaddr)
    # _conn.request('POST', '/cdnUrlPush.do', _params, headers=HTTP_HEADER)
    _conn.request('GET', url=_uri)
    _response = _conn.getresponse()
    _data = _response.read()
    #_header = _data.headers
    #_code = _data.status
    return _data

from flask import Flask
from flask import render_template as render

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World !'

@app.route('/ping')
def test(output=None):
    bb = registry_conn(server, '/v1/_ping')
    return render('test.html', output=bb)

@app.route('/search')
def search(output=None):
    bb = registry_conn(server, '/v1/search?q=arkii')
    return render('test.html', output=bb)


if __name__ == '__main__':
    Flask.debug = True
    app.run()
