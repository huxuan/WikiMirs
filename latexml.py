#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: latexml.py
Author: huxuan
Email: i(at)huxuan.org
Description: A wrapper of LaTeXML
"""

import re
from subprocess import Popen, PIPE, STDOUT

from lib import xmlclean

def latexmlmath(texmath, options=[]):
    """docstring for latexmlmath"""
    # print texmath
    # raw_input()
    commands = ['latexmlmath']
    commands.extend(options)
    commands.append('--')
    commands.append('-')
    # print commands
    popen = Popen(commands, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res = popen.communicate(texmath)[0]
    # print res
    return res

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
