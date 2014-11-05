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


import os, re, tarfile
from datetime import datetime

#from urllib2.parse import urlencode

server = '10.15.184.241'
target = '/v1/_ping'

from httplib import HTTPConnection

from flask import Flask
from flask import request
from flask import json
from flask import render_template as render


class RegistryClass:
    def __init__(self):
        self.http_header = {
            "Cache-Control": "no-cache",
            "User-Agent": "DockerRegistryUI",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        self.jsonde = json.JSONDecoder()
        self.jsonen = json.JSONEncoder()

    def ping(self, IP=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.conn.request(method='GET', url='/v1/_ping', headers=self.http_header)
            self.response = self.conn.getresponse()
            self.data = self.response.read()
            if verbose is True:
                self.data = {'Callback' : self.data}
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        finally:
            self.conn.close()
        return self.data

    def get(self, IP=None, uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.action = 'GET'
            self.conn.request(method=self.action, url=uri, headers=self.http_header)
            self.response = self.conn.getresponse()
            self.content = self.response.read() #here is str type
            self.data = self.jsonde.decode(self.content) #convert str to dict
            if verbose is True:
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        finally:
            self.conn.close()
        return self.data

    def act(self, action='GET', IP=None, uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.conn.request(method=action, url=uri, headers=self.http_header)
            self.response = self.conn.getresponse()
            self.content = self.response.read() #here is str type
            self.data = self.jsonde.decode(self.content) #convert str to dict
            if verbose is True:
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        finally:
            self.conn.close()
        return self.data

    def close(self):
        self.conn.close()

# def data2table(input):


registry = RegistryClass()


app = Flask(__name__)

@app.route('/')
def main_page():
    all = registry.get(server, '/v1/search?q=')
    # return render('index.html', msg=alli)
    return render('test.html', msg=all)


@app.route('/ping')
def ping():
    bb = registry.ping(server, verbose=True)
    return str(bb)


@app.route('/find/', methods=['POST'])
@app.route('/find/<text>')
def find_image(text=None):
    def go_search(n=None):
        l = registry.get(server, '/v1/search?q=' + str(n))
        return l

    if request.method == 'POST':
        msg = go_search(n=request.values['name'])

    if text:
        msg = go_search(n=text)

    return render('index.html', msg=msg)

@app.route('/rm/', methods=['POST'])
@app.route('/rm/<name>')
def delete(name=None):
    if request.method == 'POST':
        uri = '/v1/repositories/' + str(request.values['name'])
        msg = registry.act(server, action='DELETE' , uri=uri)
    if name:
        uri = '/v1/repositories/' + str(name)
        msg = registry.act(server, action='DELETE' , uri=uri)
    # return render('index.html', msg=msg)
    return str(msg)




@app.route('/plain', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world():
    if request.method == 'GET':
        return 'YOU GET ME !'
    if request.method == 'POST':
        return 'YOU POST ME !'
    if request.method == 'PUT':
        return 'YOU PUT ME !'
    if request.method == 'DELETE':
        return 'YOU DELETE ME !'
    else:
        return 'YOU DID NOTHING !'










if __name__ == '__main__':
    Flask.debug = True
    app.run()
