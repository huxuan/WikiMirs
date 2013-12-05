#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: config-sample.py
Author: huxuan
Email: i(at)huxuan.org
Description: Sample of needed configuration
"""

# VERSION should be 'development' or 'production'
# for 'development' it will use only the test data
# while for 'production' it will use the whole data
VERSION = 'development'

# The name of mongodb database
DBNAME = 'wikimirs'

# Collection name for generalized and raw index
COLLECTION_NAME_GEN = 'index_gen'
COLLECTION_NAME_RAW = 'index_raw'
