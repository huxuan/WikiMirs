#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lib.py
Author: huxuan
Email: i(at)huxuan.org
Description: Some common use functions
"""

import re
from xml.dom import Node
from xml.dom.minidom import parseString

OPTIONS = ['--noparse', '--quiet']

IGNORE_LATEX_LIST = [r'{}']
IGNORE_SPACE_LIST = ['^\s+', '\s+$']
IGNORE_MULTI_SPACE = '\s+'

def normalize_content(content):
    """docstring for normalize_content"""
    content = re.sub(IGNORE_MULTI_SPACE, ' ', content)
    for ignore_item in IGNORE_SPACE_LIST:
        content = re.sub(ignore_item, '', content)
    return content

def normalize_latex(latex):
    """docstring for normalize_latex"""
    for ignore_item in IGNORE_LATEX_LIST:
        latex = re.sub(ignore_item, '', latex)
    #latex = re.sub(IGNORE_MULTI_SPACE, ' ', latex)
    #latex = re.sub('(\W) ', r'\1', latex)
    #latex = re.sub(' (\W)', r'\1', latex)
    for ignore_item in IGNORE_SPACE_LIST:
        latex = re.sub(ignore_item, '', latex)
    return latex

def xml2terms(xml):
    """docstring for xml2terms"""
    root = parseString(xml).documentElement
    stack = [root, ]

    while stack:
        res = stack[-1].toxml()
        yield res, re.sub('>[^<]+?<', '><', res), len(stack)
        if stack[-1].firstChild and \
            stack[-1].firstChild.firstChild and \
            stack[-1].firstChild.firstChild.nodeType != Node.TEXT_NODE and \
            stack[-1].firstChild.nodeType != Node.TEXT_NODE:
            stack.append(stack[-1].firstChild)
        elif stack[-1].nextSibling:
            stack[-1] = stack[-1].nextSibling
        else:
            stack.pop()
            while stack and not stack[-1].nextSibling:
                stack.pop()
            if stack:
                stack[-1] = stack[-1].nextSibling

