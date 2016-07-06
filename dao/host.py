#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   Test db
#

""" Data Access Object
    This file impelements DBI for the table 'Host'

The Host table's create sql is : 

CREATE TABLE IF NOT EXISTS `test`.`Host` (
  `host_id` INT NOT NULL AUTO_INCREMENT,
  `host_type` INT NULL,
  `hostname` VARCHAR(45) NULL,
  `ip` VARCHAR(45) NULL,
  `create_time` VARCHAR(45) NULL,
  `cpu_count` INT NULL,
  `cpu_pcount` INT NULL,
  `memory` INT NULL,
  `os` VARCHAR(200) NULL,
  `comment` VARCHAR(200) NULL,
  PRIMARY KEY (`host_id`))
ENGINE = InnoDB;

"""

from util.dbconst import TableSelectSql
import logging


class HostDao:
    def __init__(self, db):
        self.db = db

    def insert_by_dict(self, host, replace=False):
        try:
            id = self.db.insert_by_dict("Host", host, replace)
            return id
        except Exception, ex:
            logging.error("Insert host failed! Exception: %s   Host: %s", str(ex), str(host))
            return None

    def if_exist(self, hostname, ip):
        ret = self.get_by_hostname(hostname)
        if ret is not None:
            return True

        ret = self.get_by_ip(ip)
        if ret is not None:
            return True

        return False

    def get_by_ip(self, ip):
        sql = TableSelectSql.HOST + " where ip='" + str(ip)+"'"
        return self.db.get(sql)

    def get_all(self):
        sql = TableSelectSql.HOST
        return self.db.query(sql)

    def get_by_hostname(self, hostname):
        sql = TableSelectSql.HOST + " where hostname='" + str(hostname)+"'"
        return self.db.get(sql)

    def get_by_id(self, host_id):
        sql = TableSelectSql.HOST + " where host_id=%s" % str(host_id)
        return self.db.get(sql)

    def get_id_by_hostname(self, hostname):
        sql = TableSelectSql.HOST + " where hostname='" + str(hostname)+"'"
        ret = self.db.get(sql)
        if ret is not None:
            return ret.host_id
        return None

    def update_worker_num_by_hostname(self, hostname, worker_num):
        try:
            sql = "UPDATE Host SET worker_num=%s WHERE hostname='%s'" % (worker_num, str(hostname))
            ret = self.db.execute(sql)
            return ret
        except Exception, ex:
            logging.error("Update Host failed! Exception: %s   hostname: %s , worker_num: %s", str(ex), str(hostname), worker_num)
            return None

    def update_worker_num_by_id(self, host_id, worker_num):
        try:
            sql = "UPDATE Host SET worker_num=%s WHERE host_id=%s" % (worker_num, host_id)
            ret = self.db.execute(sql)
            return ret
        except Exception, ex:
            logging.error("Update Host failed! Exception: %s   host_id: %s , worker_num: %s", str(ex), host_id, worker_num)
            return None

    def del_by_hostname(self, hostname):
        try:
            sql = "DELETE FROM Host WHERE hostname='" + str(hostname) + "'"
            ret = self.db.execute(sql)
            return ret
        except Exception, ex:
            logging.error("Delete host failed! Exception: %s   hostname: %s", str(ex), str(hostname))
            return None

    def del_by_id(self, host_id):
        try:
            sql = "DELETE FROM Host WHERE host_id=" + str(host_id)
            ret = self.db.execute(sql)
            return ret
        except Exception, ex:
            logging.error("Delete host failed! Exception: %s   host_id: %s", str(ex), host_id)
            return None
