#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com 
#   Date    :   2014/02/25 
#   Desc    :   Test db 
#

import logging
from util.config import Config
from util import torndb
from util.dbconst import TableFields, TableSelectSql
import util.globalvar as GlobalVar
from dao.host import HostDao

CONF_FILE = "conf/svc.conf"


# The config file parser
def parse_config(conf_file):
    # parse conf file
    conf = Config(conf_file)
    conf.load_conf()


# Init logging
def init_logging():
    sh = logging.StreamHandler()
    logger = logging.getLogger()
    logger.setLevel(Config.log_level)

    ###########This set the logging level that show on the screen#############
    # sh.setLevel(logging.DEBUG)
    # sh.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    logging.info("Current log level is : %s",
                 logging.getLevelName(logger.getEffectiveLevel()))


def test_host(db):
    dao = HostDao(db)
    host = {}
    host['hostname'] = 'test1'
    host['ip'] = '10.22.10.90'
    ret = dao.insert_by_dict(host)
    print "insert host : %s, ret: %s" % (str(host), str(ret))

    h = dao.get_by_hostname('test1')
    print "get by hostname, result:%s", str(h)

    # ret = dao.del_by_hostname('test_host')

    ret = dao.update_worker_num_by_hostname('test1', 20)
    print ret


def main():
    ############parse and load config file###############
    parse_config(CONF_FILE)

    init_logging()

    mysql_host = Config.db_host + ":" + str(Config.db_port)
    db = torndb.Connection(
        host=mysql_host, database=Config.db_name,
        user=Config.db_user, password=Config.db_pass
    )
    GlobalVar.set_db_handle(db)

    #################init db const value###################
    TableSelectSql(GlobalVar.get_db_handle())
    TableFields(GlobalVar.get_db_handle())

    test_host(db)


if __name__ == "__main__":
    main()
