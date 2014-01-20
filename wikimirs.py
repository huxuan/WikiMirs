#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: wikimirs.py
Author: huxuan
Email: i(at)huxuan.org
Description: web of wikimirs
"""

import os
import sys

import gevent.monkey
gevent.monkey.patch_all()
from bottle import run, get, post, request, template, static_file

try:
    import config
except ImportError:
    print "[Error] config.py is needed! You can refer to config-sample.py!"
    sys.exit(1)

from config import VERSION
from online import get_result

@get('/')
def index_get():
    """docstring for index_get"""
    query = request.query.query.encode('utf-8')

    if query:
        offset = int(request.query.offset or 0)
        count = int(request.query.count or 10)
        lang = str(request.query.lang or 'latex')
        res = get_result(query, offset, count, lang)

        if 'api' in request.query.search:
            return res
        else:
            return template('result', res=res, query=query)
    else:
        return template('index')

@get('/<css:re:.+\.css>')
def css_get(css):
    """
    Get css file
    """
    filename = 'views/%s' % css
    if os.path.isfile(filename):
        return static_file(css, root='views')
    else:
        return static_file('style.css', root='views')

@get('/MathJax.js')
def mathjaxjs_get():
    """Get MathJax js file"""
    return static_file('MathJax.js', root='MathJax')

@get('/<filepath:re:config/.+>')
@get('/<filepath:re:images/.+>')
@get('/<filepath:re:fonts/.+>')
@get('/<filepath:re:jax/.+>')
def mathjax_get(filepath):
    """docstring for mathjax_get"""
    return static_file(filepath, root='MathJax')

@get('/jquery-1.8.3.min.js')
def jquery_get():
    """docstring for jquery_get"""
    return static_file('jquery-1.8.3.min.js', root='views')

def main():
    """docstring for main"""
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        port = sys.argv[1]
    else:
        port = 8888
    run(server='gevent', host='0.0.0.0', port=port,
        debug=(VERSION != 'production'))

if __name__ == '__main__':
    main()
