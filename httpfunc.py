# -*- coding: utf-8 -*-
__author__ = 'arkii'
__email__ = 'sun.qingyun@zol.com.cn'
__create__ = '10/31/14 17:57'

from urllib import request
from urllib.parse import urlencode
from http.client import HTTPConnection

HTTP_HEADER = {
    "Cache-Control": "no-cache",
    "User-Agent": "SquidClient",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}


def cdn_push(node, url):
    _url = []
    if isinstance(url, list):
        _url = ','.join(url)
    else:
        _url = url
    _params = urlencode({'username': 'lb_fresh', 'password': 'ct557k3O6', 'url': _url, 'type': 1})
    _conn = HTTPConnection(node)
    _conn.request('POST', '/cdnUrlPush.do', _params, headers=HTTP_HEADER)
    _data = _conn.getresponse()
    _header = _data.headers
    _rk = RK_MAP[int(_header['rk'])]
    _code = _data.status




