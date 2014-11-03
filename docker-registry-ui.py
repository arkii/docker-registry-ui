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



import tarfile
import re
import os
from datetime import datetime

#from urllib2.parse import urlencode

server = '10.15.184.241'
target = '/v1/_ping'



from httplib import HTTPConnection

class RegistryClass:
    def __init__(self):
        self.http_header = {
            "Cache-Control": "no-cache",
            "User-Agent": "DockerRegistryUI",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }

        #self.server = '10.15.184.241'
        #self.target = '/v1/_ping'

    # def conn(self, IP):
    #     self.conn = HTTPConnection(IP)
    #     return self.conn

    def get(self, IP=None, uri=None):
        self.conn = HTTPConnection(IP)
        self.action = 'GET'
        self.conn.request(method=self.action, url=uri, headers=self.http_header)
        self.response = self.conn.getresponse()
        self.data = self.response.read()
        #self.header = self.response.headers
        #self.status = self.response.status
        self.conn.close()
        return self.data

    def close(self):
        self.conn.close()

    # def registry_act(self):


registry = RegistryClass()
# registry.conn(server)



from flask import Flask
from flask import request
from flask import json
from flask import render_template as render

app = Flask(__name__)


@app.route('/plain', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return 'YOU POST ME !'
    else:
        return 'YOU GET ME !'



@app.route('/')
def main_page():
    allimage = registry.get(server, '/v1/search?q=')
    msg = json.JSONDecoder(allimage).decode
    return render('index.html', msg=msg)

@app.route('/ping')
def test():
    bb = registry.get(server, '/v1/_ping')
    return render('index.html', msg=bb)

@app.route('/search/', methods=['POST'])
@app.route('/search/<imagename>')
def search_image(imagename=None):
    def go_search(n=None):
        l = registry.get(server, '/v1/search?q=' + str(n))
        return l

    if request.method == 'POST':
        _content = go_search(n=request.values['imagename'])

    if imagename:
        _content = go_search(n=imagename)
    return render('index.html', msg=_content)

#registry.close()

if __name__ == '__main__':
    Flask.debug = True
    app.run()
