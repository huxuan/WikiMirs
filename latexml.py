#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: latexml.py
Author: huxuan
Email: i(at)huxuan.org
Description: A wrapper of LaTeXML
"""

import re
import subprocess

WHITESPACE_PATTERN = re.compile(r'\s+', re.MULTILINE)
MATH_PATTERN = re.compile(r'<math.*?>(.*?)</math>',
    re.MULTILINE | re.IGNORECASE | re.DOTALL)

class LaTeXMLException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def xmlclean(xml):
    """docstring for xmlclean"""
    # Filter tags' attributes
    xml = re.sub('(<\S+?)\ [^>]*?(\/?>)', r'\1\2', xml)
    # Filter whitespace characters
    xml = re.sub('\s+', '', xml)

    res = MATH_PATTERN.search(xml)
    if res:
        return res.group(1)
    else:
        raise LaTeXMLException("No Valid MathML Extracted")

def latexmlmath(texmath, options=[]):
    """docstring for latexmlmath"""
    commands = ['latexmlmath']
    commands.extend(options)
    commands.append('--')
    commands.append(texmath)
    return subprocess.check_output(commands)

def latex2presentationmathml(texmath, options=[]):
    """docstring for latex2presentationmathml"""
    options.append('--presentationmathml=-')
    return latexmlmath(texmath, options)

def latex2pmml(texmath, options=[]):
    """docstring for latex2pmml"""
    pmml = latex2presentationmathml(texmath, options)
    return xmlclean(pmml)

def latex2contentmathml(texmath, options=[]):
    """docstring for latex2contentmathml"""
    options.append('--contentmathml=-')
    return latexmlmath(texmath, options)

def latex2cmml(texmath, options=[]):
    """docstring for latex2cmml"""
    cmml = latex2contentmathml(texmath, options)
    return xmlclean(cmml)

def main():
    """docstring for main"""
    texmath = '\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}'
    # print latexmlmath(texmath)
    # print latex2presentationmathml(texmath)
    # print latex2contentmathml(texmath)
    # print repr(latex2pmml(texmath))
    # print repr(latex2cmml(texmath))
    raw_input("Done!")

if __name__ == '__main__':
    main()
