# -*- coding: utf-8 -*-
__author__ = 'arkii'
__email__ = 'sun.qingyun@zol.com.cn'
__create__ = '11/11/14 17:21'



def extract(d):
    if isinstance(d, dict):
        if d.has_key('result') : print 'result', ' -is:- ', d['result']
        if d.has_key('query') : print 'query', ' -is:- ', d['query']
        if d.has_key('num_results') : print 'num_results', ' -is:- ', d['num_results']
        if d.has_key('server_headers') : print 'server_headers', ' -is:- ', d['server_headers']
        if d.has_key('server_message') : print 'server_message', ' -is:- ', d['server_message']
        if d.has_key('server_code') : print 'server_code', ' -is:- ', d['server_code']
        if d.has_key('results'):
            for i in d['results']:
                for k,v in i.iteritems():
                    print k, ' -is:- ', v
    else:
        print 'aaa'


@app.route('/')
def main_page():
    msg = registry.get(server, '/v1/search?q=', verbose=True)
    return render('test.html', msg=all, extract=lambda d: extract(d))