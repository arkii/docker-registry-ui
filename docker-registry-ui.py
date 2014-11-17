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
from urllib import urlencode

server = '10.15.184.241'
# server = ['docker-hub', 'docker-repo.alias.pch.net']
target = '/v1/_ping'

from httplib import HTTPConnection

from flask import Flask
from flask import request
from flask import json
from flask import render_template as render
from flask import make_response

def add_http_header(object=None, key=None, value=None):
    _response = make_response(object)
    _response.headers[key] = value
    return _response


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
                self.data = {'result': self.data}
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        except IOError:
            self.data = 'socket.error'
        finally:
            self.conn.close()
        return self.data


    def get(self, IP=None, uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.action = 'GET'
            self.conn.request(method=self.action, url=uri, headers=self.http_header)
            self.response = self.conn.getresponse()
            self.content = self.response.read()  # here is str type
            self.data = self.jsonde.decode(self.content)  # convert str to dict
            if verbose is True:
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        except IOError:
            self.data = 'socket.error'
        finally:
            self.conn.close()
        return self.data

    def act(self, IP=None, action='GET', uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.method = action
            self.conn.request(method=self.method, url=uri, headers=self.http_header)
            self.response = self.conn.getresponse()
            self.content = self.response.read()  # here is str type
            self.data = self.jsonde.decode(self.content)  # convert str to dict
            if verbose is True:
                self.data = {'result': self.data}
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        except IOError:
            self.data = 'socket.error'
        finally:
            self.conn.close()
        return self.data

    def delete(self, IP=None, action='DELETE', uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(IP, port=80, timeout=3)
            self.method = action
            self.conn.request(method=self.method, url=uri, headers=self.http_header)
            self.response = self.conn.getresponse()
            self.content = self.response.read()  # here is str type
            self.data = self.content
            if verbose is True:
                self.data = {'result': self.data}
                self.status = self.response.status
                self.message = self.response.reason
                self.headers = dict(self.response.getheaders())
                self.data['server_headers'] = self.headers
                self.data['server_message'] = self.message
                self.data['server_code'] = self.status
        except IOError:
            self.data = 'socket.error'
        finally:
            self.conn.close()
        return self.data

    def close(self):
        self.conn.close()


registry = RegistryClass()

app = Flask(__name__)


@app.route('/')
def main_page():
    _registryhost = server
    _status = ping_server()
    _t = registry.get(server, '/v1/search?q=')
    _imagenumber = ''
    if isinstance(_t, dict): _imagenumber = _t['num_results']

    return render('index.html', pagetitle='index', imagenumber=_imagenumber, hosts=_registryhost, status=_status)


@app.route('/images')
def images_page():
    msg = registry.get(server, '/v1/search?q=')
    _tableheader = ['Name', 'Description', 'Tags', 'Actions']
    return render('images.html', pagetitle='images', msg=msg, tableheader=_tableheader)


@app.route('/ping')
def ping_server():
    return registry.ping(server)


@app.route('/find/', methods=['POST'])
@app.route('/find/<text>')
def find_image(text=None):
    if request.method == 'POST':
        uri = '/v1/search?q=' + request.values['name']
    if text:
        uri = '/v1/search?q=' + str(text)
    msg = registry.get(server, uri=uri, verbose=True)
    _tableheader = ['Name', 'Description', 'Tags', 'Actions']
    return render('images.html', pagetitle='images', msg=msg, tableheader=_tableheader)


@app.route('/info/<id>')
def show_info(id=None):
    _uri = '/v1/images/' + id + '/json'
    _msg = registry.act(server, uri=_uri, verbose=True)
    _msg['tableheader'] = ['Tag', 'ID']
    _uri = '/v1/images/' + id + '/ancestry'
    _ancestry = {}
    _ancestry['tableheader'] = 'Ancestry'
    _ancestry['data'] = registry.act(server, uri=_uri)
    return render('info.html', pagetitle='images', msg=_msg, ancestry=_ancestry)


@app.route('/tags/', methods=['POST'])
@app.route('/tags/<namespace>/<repository>')
def show_tags(namespace=None, repository=None):
    if repository is not None: _query = namespace + '/' + repository
    uri = '/v1/repositories/' + _query + '/tags'
    if request.method == 'POST': uri = '/v1/repositories/' + str(request.values['name']) + '/tags'
    msg = registry.act(server, uri=uri, verbose=True)
    msg['tableheader'] = ['Tag', 'ID']
    _tree_json = '/json/' + _query
    return render('tags.html', pagetitle='images', tree_json=_tree_json, msg=msg)


@app.route('/rm/', methods=['POST'])
@app.route('/rm/<namespace>/<repository>')
@app.route('/rm/<namespace>/<repository>/<tag>')
def delete(namespace=None, repository=None, tag=None):
    if request.method == 'POST':
        uri = '/v1/repositories/' + str(request.values['name']) + '/'
    else:
        if namespace is not None: _query = namespace + '/'
        if repository is not None: _query = namespace + '/' + repository + '/'
        if tag is not None: _query = namespace + '/' + repository + '/tags/' + tag
        uri = '/v1/repositories/' + _query
    msg = registry.delete(server, action='DELETE', uri=uri)
    # msg['tableheader'] = ['Tag', 'ID']
    # return render('tags.html', pagetitle='images', msg=msg)
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
        return 'YOU DELETE ME   !'
    else:
        return 'YOU DID NOTHING    !'


@app.route('/test')
def test():
    return render('test.html')


@app.route('/tree')
def tree():
    _url = '/json'
    return render('tree.html', tree_json=_url)

@app.route('/json/<namespace>/<repository>')
def output_json(namespace=None, repository=None):
    if repository is not None: _query = namespace + '/' + repository
    _uri = '/v1/repositories/' + _query + '/tags'
    _ancestry = {}
    _ancestry['tableheader'] = 'Ancestry'
    _ancestry['data'] = registry.act(server, uri=_uri)
    _tree_json = _ancestry['data']
    _d = {'name':_query}
    _c = []
    for k, v in _tree_json.iteritems():
        _c.append({'name':k, 'children':[{'name':v}]})
    _d['children'] = _c
    _data = json.JSONEncoder().encode(_d)
    return add_http_header(_data,'Content-Type', 'application/json')









if __name__ == '__main__':
    # Flask.debug = True
    # app.run(host='0.0.0.0')
    app.run(debug=1)