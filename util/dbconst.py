#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   Test db
#
#

class TableName:
    HOST = "Host"

class TableFields:
    HOST = None

    def __init__(self, db):
        TableFields.HOST = db.get_fields_str(TableName.HOST)

class TableSelectSql:
    HOST = None

    def __init__(self, db):
        TableSelectSql.HOST = db.get_select_sql(TableName.HOST)
