#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: lib.py
Author: huxuan
Email: i(at)huxuan.org
Description: Some common use functions
"""

import re
import zlib
import base64
from xml.dom import Node
from xml.dom.minidom import parseString

OPTIONS = ['--noparse', '--quiet']

IGNORE_LATEX_LIST = [r'\\qquad', r'\\quad', r'\\\\\[\w+\]', r'\\\\', r'\\!',
            r'\\,', r'\\;', r'\\ ', r'{}', ]
IGNORE_SPACE_LIST = ['^\s+', '\s+$']
IGNORE_MULTI_SPACE = '\s+'

MATH_PATTERN = re.compile(r'<math>(.*?)</math>',
    re.MULTILINE | re.IGNORECASE | re.DOTALL)

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

def term_compress(term):
    """docstring for term_compress"""
    return base64.b64encode(zlib.compress(term.encode('utf8')))

def term_decompress(term):
    """docstring for term_decompress"""
    return zlib.decompress(base64.b64decode(term)).decode('utf8')

def xml2terms(xml):
    """docstring for xml2terms"""
    root = parseString(xml).documentElement
    stack = [root, ]

    while stack:
        if stack[-1].firstChild and \
            stack[-1].firstChild.nodeType != Node.TEXT_NODE:
            term_raw = stack[-1].toxml()
            term_gen = re.sub('>[^<]+?<', '><', term_raw);
            # print term_raw, term_gen, len(stack)
            term_raw = term_compress(term_raw)
            term_gen = term_compress(term_gen)
            # print term_raw, term_gen, len(stack)
            yield term_raw, term_gen, len(stack)
        if stack[-1].firstChild and \
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

def xmlclean(xml):
    """docstring for xmlclean"""
    # Filter tags' attributes
    xml = re.sub('(<[^>\s]+?)\ [^>]*?(\/?>)', r'\1\2', xml)
    # Filter whitespace characters
    xml = re.sub('\s+', '', xml)

    res = MATH_PATTERN.search(xml)
    if res:
        return res.group(1)
    else:
        return xml
