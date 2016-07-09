# -*- coding: utf-8 -*-
__author__ = 'arkii'
__email__ = 'sun.qingyun@zol.com.cn'
__create__ = '10/30/14 19:48'


import os, re, json
from urllib import urlencode
from httplib import HTTPConnection
from flask import render_template as render
from flask import make_response

def add_http_header(object=None, key=None, value=None):
    _response = make_response(object)
    _response.headers[key] = value
    return _response

class RegistryClass:
    def __init__(self, server, port):
        self.http_header = {
            "Cache-Control": "no-cache",
            "User-Agent": "DockerRegistryUI",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "text/plain"
        }
        self.jsonde = json.JSONDecoder()
        self.jsonen = json.JSONEncoder()
        self.server = server
        self.port = port

    def ping(self, verbose=False):
        try:
            self.conn = HTTPConnection(self.server, port=self.port, timeout=3)
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


    def get(self, uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(self.server, port=self.port, timeout=3)
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

    def act(self, action='GET', uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(self.server, port=self.port, timeout=3)
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

    def delete(self, action='DELETE', uri=None, verbose=False):
        try:
            self.conn = HTTPConnection(self.server, port=self.port, timeout=3)
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


ip  = '101.200.125.9'
port= 5000
registry = RegistryClass(server=ip, port=port)

import requests
from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)
uri = "http://" + ip + ':' + str(port)
timeout = 3
RegistryHost = []
RegistryHost_default = uri


@app.route('/')
def index():
    path = '/v1/search'
    res  = requests.get(uri+path, timeout=timeout)
    data = res.json()
    return render_template('index.html', data=data, hosts=uri, version='v1')


@app.route('/registry_manager', methods=["GET", "POST", "DELETE", "PUT"])
def registry_manager():
    method = request.method
    if method == "GET":
        return jsonify(RegistryHost=RegistryHost)
    elif method == "POST":
        _add_registry_host = request.form.get("registry_host")
        RegistryHost.append(_add_registry_host)
        return redirect(url_for("registry_manager"))
    elif method == "DELETE":
        _del_registry_host = request.form.get("registry_host")
        for host in RegistryHost:
            if host.find("_del_registry_host") >= 0:
                RegistryHost.remove(_del_registry_host)
                return redirect(url_for("registry_manager"))
            else:
                return "no such registry"
    elif method == "PUT":
        pass


@app.route('/images/', methods=['GET','POST'])
@app.route('/images/<text>', methods=['GET','POST'])
@app.route('/find/', methods=['GET','POST'])
@app.route('/find/<text>', methods=['GET','POST'])
def images_page(text=None):
    path = "/v1/search"
    if request.method == 'POST':
        path = '/v1/search?q=' + request.form.get('search')
    if text:
        path = '/v1/search?q=' + str(text)
    res  = requests.get(uri+path, timeout=timeout)
    data = res.json()
    return render_template('images.html', data=data)


@app.route('/info/<image_id>')
def show_info(image_id=None):
    data = {}
    json_url = uri + '/v1/images/' + image_id + '/json'
    ance_url = uri + '/v1/images/' + image_id + '/ancestry'
    data["json"]     = requests.get(json_url, timeout=timeout).json()
    data["ancestry"] = requests.get(ance_url, timeout=timeout).json()
    return render_template('info.html', data=data)


@app.route('/ping')
def ping_server():
    res  = requests.get(uri+'/_ping', timeout=1)
    data = res.json()
    return jsonify({uri: data})

@app.route('/tags/', methods=['POST'])
@app.route('/tags/<namespace>/<repository>')
def show_tags(namespace=None, repository=None):
    if repository is not None: _query = namespace + '/' + repository
    if request.method == 'POST': _query = str(request.values['name'])
    uri = '/v1/repositories/' + _query + '/tags'
    msg = registry.act(uri=uri, verbose=True)
    _tableheader = ['Name', 'ID', 'Actions']
    _tree_json = '/json/' + _query
    return render('tags.html', pagetitle='tags', tree_json=_tree_json, msg=msg, tableheader=_tableheader, reponame=_query)


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
    msg = registry.delete(action='DELETE', uri=uri)
    # msg['tableheader'] = ['Tag', 'ID']
    # return render('tags.html', pagetitle='images', msg=msg)
    return str(msg)


@app.route('/json/<namespace>/<repository>')
def output_json(namespace=None, repository=None):
    if repository is not None: _query = namespace + '/' + repository
    _uri = '/v1/repositories/' + _query + '/tags'
    _ancestry = {}
    _ancestry['tableheader'] = 'Ancestry'
    _ancestry['data'] = registry.act(uri=_uri)
    _tree_json = _ancestry['data']
    _d = {'name':_query}
    _c = []
    for k, v in _tree_json.iteritems():
        _c.append({'name':k, 'children':[{'name':v}]})
    _d['children'] = _c
    _data = json.JSONEncoder().encode(_d)
    return add_http_header(_data,'Content-Type', 'application/json')

if __name__ == '__main__':
    from config import GLOBAL
    Host = GLOBAL.get('Host')
    Port = GLOBAL.get('Port')
    app.run(host=Host, port=int(Port), debug=True)