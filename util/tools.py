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

"""

"""
import logging
from datetime import date, datetime


def strip_string(ori):
    # if isinstance(ori, str):
    if ori is None:
        return ori

    ori = str(ori)
    ori = ori.strip("\'")
    ori = ori.strip("\"")
    return ori


def to_int(num):
    if num is None:
        return num

    try:
        num = strip_string(num)
        value = int(num)
        return value
    except Exception, ex:
        logging.error("Convert '%s' to Int Error: %s", str(num), str(ex))
        return None


def to_encode(ustr, encoding='utf-8'):
    if ustr is None:
        return ''
    if isinstance(ustr, unicode):
        return ustr.encode(encoding, 'ignore')
    else:
        return str(ustr)


def json_date_default(obj):
    if isinstance(obj, datetime):
        # return obj.strftime('%Y-%m-%d %H:%M:%S')
        return str(obj)
    elif isinstance(obj, date):
        # return obj.strftime('%Y-%m-%d')
        return str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)
