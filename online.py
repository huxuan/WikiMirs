#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: online.py
Author: huxuan
Email: i(at)huxuan.org
Description: online process to handle query
"""

try:
    from config import COLLECTION_NAME_RAW, COLLECTION_NAME_GEN
except ImportError:
    print "[Error] config.py is needed! You can refer to config-sample.py!"
    sys.exit(1)

import sys
import math
import urllib
import datetime
from operator import itemgetter

from lib import OPTIONS
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

def get_score(latex):
    """docstring for get_score"""

    latex = normalize_latex(latex)

    pmml = latex2pmml(latex, OPTIONS)

    res = {}

    score_max = 0

    time_begin = datetime.datetime.utcnow()

    for term_raw, term_gen, level in xml2terms(pmml):

        index_term = {
                cnraw: term_raw,
                cngen: term_gen,
            }

        for index, term in index_term.iteritems():

            index_item = db[index].find_one({'term': term})
            if index_item:
                count_pmml = len(index_item['index'])
                for pmml_id, attrs in index_item['index'].iteritems():
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

                    res[pmml_id] = res.get(pmml_id, 0) + \
                        score_tf * score_idf * score_level * score_nor
                    score_max = max(score_max, res[pmml_id])

    time_end = datetime.datetime.utcnow()

    bottom = score_max / 20
    res = filter(lambda x: x[1] > bottom, res.iteritems())
    while len(res) > 100:
        bottom *= 1.1
        res = filter(lambda x: x[1] > bottom, res)
    res = sorted(res, key=itemgetter(1), reverse=True)

    return res, time_end - time_begin

def get_result(query, offset=0, count=10):
    """docstring for get_resule"""
    res = {'entry_list': []}

    try:
        score_list, res['time'] = get_score(query)
        res['time'] = str(res['time']) + 's'
        res['offset'] = offset
        res['count'] = count
        if offset >= count:
            res['previous'] = urllib.urlencode({
                'query': query,
                'offset': offset - count,
                'count': count,
            })
        res['next'] = urllib.urlencode({
            'query': query,
            'offset': offset + count,
            'count': count,
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
    except Exception, exc:
        res['error'] = str(exc)

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
