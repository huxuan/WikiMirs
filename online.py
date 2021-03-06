#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: online.py
Author: huxuan
Email: i(at)huxuan.org
Description: online process to handle query
"""

import sys
try:
    from config import COLLECTION_NAME_RAW, COLLECTION_NAME_GEN
except ImportError:
    print "[Error] config.py is needed! You can refer to config-sample.py!"
    sys.exit(1)

import math
import urllib
import datetime
from operator import itemgetter

from lib import OPTIONS
from lib import xmlclean
from lib import xml2terms
from lib import normalize_latex
from latexml import latex2pmml

from mongodb import MONGODB as db
from mongodb import ObjectId
from config import COLLECTION_NAME_GEN as cngen
from config import COLLECTION_NAME_RAW as cnraw

TOT_PMML = db.pmml.count()
NOR_VALUE = {
    COLLECTION_NAME_RAW: 1.0,
    COLLECTION_NAME_GEN: 0.5,
}

def get_score(query, lang='latex'):
    """docstring for get_score"""

    if lang == 'latex':
        query = normalize_latex(query)
        query = latex2pmml(query, OPTIONS)
    elif lang == 'pmml':
        query = xmlclean(query)

    res = []
    score_pmml = {}
    pmml_page = {}
    score_max = 0

    time_begin = datetime.datetime.utcnow()

    for term_raw, term_gen, level in xml2terms(query):

        index_term = {
                cnraw: term_raw,
                cngen: term_gen,
            }

        for index, term in index_term.iteritems():

            index_item = db[index].find_one({'term': term})
            if index_item:
                count_pmml = len(index_item['index'])
                for page_pmml_id, attrs in index_item['index'].iteritems():
                    page_id, pmml_id = page_pmml_id.split('+')
                    pmml_page[pmml_id] = page_id
                    fileds = {'term_count': 1}
                    term_count = db.pmml.find_one(
                        ObjectId(pmml_id), fileds
                    ).values()[0]

                    score_tf = 1.0 * len(attrs) / term_count
                    score_idf = math.log(1.0 * TOT_PMML / count_pmml)
                    score_level = max(
                        1.0 / (1.0 + math.fabs(level - attr['level']))
                        for attr in attrs
                    )
                    score_nor = NOR_VALUE[index]

                    score_pmml[pmml_id] = score_pmml.get(pmml_id, 0) + \
                        score_tf * score_idf * score_level * score_nor
                    score_max = max(score_max, score_pmml[pmml_id])

    bottom = score_max / 20
    score_pmml = filter(lambda x: x[1] > bottom, score_pmml.iteritems())
    while len(score_pmml) > 200:
        bottom *= 1.01
        score_pmml = filter(lambda x: x[1] > bottom, score_pmml)
    score_pmml = sorted(score_pmml, key=itemgetter(1), reverse=True)

    page_ids = set()
    for pmml_id, score in score_pmml:
        page_id = pmml_page[pmml_id]
        if page_id not in page_ids:
            page_ids.add(page_id)
            res.append((pmml_id, score))

    time_end = datetime.datetime.utcnow()

    return res, time_end - time_begin

def get_result(query, offset=0, count=10, lang='latex'):
    """docstring for get_result"""
    res = {'entry_list': []}

    # try:
    score_list, res['time'] = get_score(query, lang)
    res['time'] = str(res['time']) + 's'
    res['offset'] = offset
    res['count'] = count
    if offset >= count:
        res['previous'] = urllib.urlencode({
            'query': query,
            'offset': offset - count,
            'count': count,
            'lang': lang,
        })
    res['next'] = urllib.urlencode({
        'query': query,
        'offset': offset + count,
        'count': count,
        'lang': lang,
    })
    for pmml_id, score in score_list[offset : offset + count]:

        fileds = {'pmml': 1, 'page_id': 1}
        pmml_item = db.pmml.find_one(ObjectId(pmml_id), fileds)
        fileds = {'title': 1}
        title = db.page.find_one(pmml_item['page_id'], fileds)['title']
        res['entry_list'].append({
            'pmml': pmml_item['pmml'],
            'score': score,
            'title': title,
        })
    # except Exception, exc:
    #     res['error'] = str(exc)

    return res

def main():
    """docstring for main"""
    if len(sys.argv) == 2:
        score_list, time_used = get_score(sys.argv[1])
    print score_list
    print len(score_list)
    print time_used

if __name__ == '__main__':
    main()
