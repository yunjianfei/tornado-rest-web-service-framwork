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

import ConfigParser
import string,os,sys
import logging


class Config:
    #####################mysql config######################
    db_name = None
    db_host = None
    db_port = None
    db_user = None
    db_pass = None
    
    #####################log config########################
    log_level = None
    log_path = None

    #####################default value config########################

    ###init func###
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.cf = None

    ###load config###
    def load_conf(self):
        if os.path.isfile(self.conf_file):

            self.cf = ConfigParser.ConfigParser()
            self.cf.read(self.conf_file)

            ## get mysql config
            Config.db_name = self.get_db_name()
            Config.db_host = self.get_db_host()
            Config.db_port = self.get_db_port()
            Config.db_user = self.get_db_user()
            Config.db_pass = self.get_db_pass()

            ## get log config
            Config.log_level = self.get_log_level()
            Config.log_path = self.get_log_path()

            return 0
        else:
            return -1
    
    def get_db_name(self):
        '''  get mysql db name '''
        return self.cf.get("db", "db_name") 

    def get_db_host(self):
        '''  get mysql db host '''
        return self.cf.get("db", "db_host") 

    def get_db_port(self):
        '''  get mysql db port '''
        return self.cf.get("db", "db_port") 

    def get_db_user(self):
        '''  get mysql db username '''
        return self.cf.get("db", "db_user") 

    def get_db_pass(self):
        '''  get mysql db password '''
        return self.cf.get("db", "db_pass") 


    def get_log_path(self):
        '''  get log path '''
        path = self.cf.get("log", "log_path") 
        if path == "" or path == None or not os.path.exists(path):
            return os.path.join(os.getcwd(), "log")
        else:
            return path

    def get_log_level(self):
        '''  get log path '''
        level = self.cf.get("log", "log_level")
        if level == "DEBUG":
            return logging.DEBUG
        elif level == "INFO":
            return logging.INFO
        elif level == "WARNING":
            return logging.WARNING
        elif level == "ERROR":
            return logging.ERROR
        else:
            return logging.INFO
