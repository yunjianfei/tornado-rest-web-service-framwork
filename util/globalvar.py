#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   
#   E-mail  :   
#   Date    :   2014/02/25 
#   Desc    :
#

class GlobalVar:
    db_handle = None
    mq_client = None

def set_db_handle(db):
    GlobalVar.db_handle = db

def get_db_handle():
    return GlobalVar.db_handle

def set_mq_client(mq_cli):
    GlobalVar.mq_client = mq_cli

def get_mq_client():
    return GlobalVar.mq_client
