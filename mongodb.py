#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: mongodb.py
Author: huxuan
Email: i(at)huxuan.org
Description: Wrapper of MongoDB python driver - pymongo
"""

from pymongo import MongoClient
from bson.objectid import ObjectId

from config import DBNAME

CONNECTION = MongoClient()
MONGODB = CONNECTION[DBNAME]

def drop_database():
    """docstring for drop_database"""
    CONNECTION.drop_database(DBNAME)
