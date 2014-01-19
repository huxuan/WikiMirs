#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: offline.py
Author: huxuan
Email: i(at)huxuan.org
Description: Offline process to build index
"""

import sys
try:
    import config
except ImportError:
    print "[Error] config.py is needed! You can refer to config-sample.py!"
    sys.exit(1)

import re
import datetime
from xml.sax import parse, SAXException
from xml.sax.handler import ContentHandler
from multiprocessing import Pool

from lib import OPTIONS
from lib import xml2terms
from lib import normalize_latex
from lib import normalize_content
from latexml import latex2pmml

from mongodb import MONGODB as db
from mongodb import drop_database
from config import COLLECTION_NAME_GEN as cngen
from config import COLLECTION_NAME_RAW as cnraw

DATA = 'data/Wikipedia-%s.xml' % config.VERSION
MATH_PATTERN = re.compile(r'<math>(.*?)</math>', re.I | re.M | re.S)

LATEX_HACK = [
    u"\\begin{pmatrix} \\frac{1}{c}\\frac{\\partial \\phi}{\\partial t'} & \\frac{\\partial \\phi}{\\partial x'} & \\frac{\\partial \\phi}{\\partial y'} & \\frac{\\partial \\phi}{\\partial z'}\\end{pmatrix} = \\begin{pmatrix} \\frac{1}{c}\\frac{\\partial \\phi}{\\partial t} & \\frac{\\partial \\phi}{\\partial x} & \\frac{\\partial \\phi}{\\partial y} & \\frac{\\partial \\phi}{\\partial z}\\end{pmatrix}\\begin{pmatrix}\n\\gamma & -\\beta\\gamma & 0 & 0\\\\\n-\\beta\\gamma & \\gamma & 0 & 0\\\\\n0 & 0 & 1 & 0\\\\\n0 & 0 & 0 & 1\n\\end{pmatrix} \\,.",
    u'\\begin{align}\n{\\mathbf{A=LDL}^\\mathrm{T}} & =\n\\begin{pmatrix}\n \\mathbf I & 0 & 0 \\\\\n \\mathbf L_{21} & \\mathbf I & 0 \\\\\n \\mathbf L_{31} & \\mathbf L_{32} & \\mathbf I\\\\\n\\end{pmatrix}\n\\begin{pmatrix}\n \\mathbf D_1 & 0 & 0 \\\\\n 0 & \\mathbf D_2 & 0 \\\\\n 0 & 0 & \\mathbf D_3\\\\\n\\end{pmatrix}\n\\begin{pmatrix}\n \\mathbf I & \\mathbf L_{21}^\\mathrm T & \\mathbf L_{31}^\\mathrm T \\\\\n 0 & \\mathbf I & \\mathbf L_{32}^\\mathrm T \\\\\n 0 & 0 & \\mathbf I\\\\\n\\end{pmatrix} \\\\\n& = \\begin{pmatrix}\n \\mathbf D_1 &   &(\\mathrm{symmetric})   \\\\\n \\mathbf L_{21} \\mathbf D_1 & \\mathbf L_{21} \\mathbf D_1 \\mathbf L_{21}^\\mathrm T + \\mathbf D_2& \\\\\n \\mathbf L_{31} \\mathbf D_1 & \\mathbf  L_{31} \\mathbf D_{1} \\mathbf L_{21}^\\mathrm T + \\mathbf  L_{32} \\mathbf D_2 & \\mathbf L_{31} \\mathbf D_1 \\mathbf L_{31}^\\mathrm T + \\mathbf L_{32} \\mathbf D_2 \\mathbf L_{32}^\\mathrm T + \\mathbf D_3\n\\end{pmatrix}\n\\end{align}\n',
]

class WikiMathHandler(ContentHandler):
    """Summary of WikiMathHandler"""
    def __init__(self, *args, **kwargs):
        """Init WikiMathHandler"""
        self.tag = ''
        self.title = ''
        self.text = ''
        self.con_list = []
        self.page_id = None
        self.pmml_count = 0
        self.pool = Pool(processes=20)

    def startElement(self, name, attrs):
        """docstring for startElement"""
        self.tag = name
        # print name, attrs
        # raw_input()
        if name == 'page':
            self.page_id = db.page.save({})

    def endElement(self, name):
        """docstring for endElement"""
        if name == 'page':
            db.page.save({
                '_id': self.page_id,
                'title': self.title,
            })
        elif name == 'title':
            self.title = normalize_content(''.join(self.con_list))
            del self.con_list[:]

            # Update self.pmml_count when the count has an evident increase
            pmml_count = db.pmml.count()
            if pmml_count - self.pmml_count > 100:
                self.pmml_count = pmml_count
                print pmml_count

            # if pmml_count >= 100000:
            #     raise SAXException('Get %d latex snippets' % pmml_count)
            # print self.title

        elif name == 'text':
            self.text = ''.join(self.con_list)
            self.text = re.sub('<!--.*?-->', '', self.text)
            del(self.con_list[:])

            # print len(self.text)
            latex_list = MATH_PATTERN.findall(self.text)
            # print len(latex_list)
            for latex in latex_list:
                self.pool.apply_async(work, (latex, self.page_id, self.title))

    def characters(self, content):
        """docstring for characters"""
        if self.tag in ('title', 'text'):
            self.con_list.append(content)
            # print repr(content)
            # raw_input()

def work(latex, page_id, title):
    """docstring for work"""
    # try:
    if latex in LATEX_HACK:
        return
    # print repr(latex)
    latex = normalize_latex(latex)
    # print repr(latex)
    pmml = latex2pmml(latex.encode('utf8'), list(OPTIONS))
    # print repr(pmml)
    # raw_input()
    if pmml:
        pmml_id = db.pmml.save({
            'page_id': page_id,
            'pmml': pmml,
        })
        term_count = 0
        for term_raw, term_gen, level in xml2terms(pmml):
            attr = {'level': level}
            modification = {
                '$inc': {'count': 1},
                '$push': {'index.%s+%s' % (page_id, pmml_id): attr},
            }

            # print "len(term_raw): ", len(term_raw)
            # print "len(term_gen): ", len(term_gen)
            condition = {'term': term_raw}
            db[cnraw].update(condition, modification, True)
            condition = {'term': term_gen}
            db[cngen].update(condition, modification, True)
            term_count += 2
        db.pmml.update(
            {'_id': pmml_id},
            {'$set': {'term_count': term_count}}
        )
    # except Exception, exc:
    #     print 'There is an error here!'
    #     f = file('error.log', 'a')
    #     print >>f, '=' * 80
    #     print >>f, 'Title:', title.encode('utf8')
    #     print >>f, 'LaTeX:', latex.encode('utf8')
    #     print >>f, 'Error:', str(exc).encode('utf8')
    #     print >>f, '=' * 80
    #     print >>f
    #     f.close()

def main():
    """docstring for main"""

    # MongoDB init
    drop_database()
    db[cnraw].create_index('term')
    db[cngen].create_index('term')

    time_begin = datetime.datetime.utcnow()

    # Begin parse
    try:
        parse(DATA, WikiMathHandler())
    except SAXException, exc:
        print exc.getMessage()
        pass
    except KeyboardInterrupt:
        pass

    time_end = datetime.datetime.utcnow()

    print "Time used for index:",  time_end - time_begin

if __name__ == '__main__':
    main()
