#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   
#

"""  

Usecase:
    ./master --port=9999

Below are some notices :

1)Master supply core WebService 
2)Master can start one or more.
3)You can set the DNS server when started more than one Master, and set Round-Robin function for load-banlance. 
4)You can use Supervisor and Nginx to lauch Master
5)If you what change some config, you can find the config dir by the variable 'CONF_FILE' in this file, and modify the config file.
6)All logs write by the logging module will be write in the log dir. One day for a log file, there can be most 10 files. Oldest file will be drop.


"""

import string,os,sys,logging,signal,time
import tornado.httpserver
import tornado.ioloop
import tornado.web

from util.options import define,options
from util.config import Config
from util import torndb
from util.dbconst import TableName,TableFields,TableSelectSql
import util.globalvar as GlobalVar

from service.host import HostHandler

MODULE="master"
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

CONF_FILE="conf/svc.conf"

#Define command parameter
define("port", default=None, help="Run server on a specific port, mast input", type=int)

#The config file parser
def parse_config(conf_file):
    #parse conf file
    conf = Config(conf_file)
    conf.load_conf()

#Init logging
def init_logging(port):
    log_file = MODULE + "." + str(port) + ".log"
    logger = logging.getLogger()
    logger.setLevel(Config.log_level)

    #fh = logging.FileHandler(os.path.join(Config.log_path, log_file)) 
    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(Config.log_path, log_file), when='D', backupCount=10) 
    sh = logging.StreamHandler()

    ###########This set the logging level that show on the screen#############
    #sh.setLevel(logging.DEBUG)
    #sh.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    fh.setFormatter(formatter) 
    sh.setFormatter(formatter) 

    logger.addHandler(fh)
    logger.addHandler(sh)
    logging.info("Current log level is : %s",logging.getLevelName(logger.getEffectiveLevel()))


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.info('Stopping http server')
    http_server.stop()

    logging.info('Master will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            GlobalVar.get_db_handle().close()
            GlobalVar.get_mq_client().disconnect()
            logging.info('Shutdown')

    stop_loop()

class MainHandler(tornado.web.RequestHandler):
    """docstring for MainHandler"""
    def get(self):
        self.write("This is SohuVideoCloud Master!")

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            debug=True,
        )

        handlers = [
            (r"/", MainHandler),
            (r"/host", HostHandler),
        ]

        mysql_host = Config.db_host + ":" + str(Config.db_port)
        self.db = torndb.Connection(
            host=mysql_host, database=Config.db_name,
            user=Config.db_user, password=Config.db_pass
        )

        GlobalVar.set_db_handle(self.db)

        super(Application,self).__init__(handlers,**settings)
    
def main():
    #################parse command#######################
    options.parse_command_line()

    if options.port == None:
        options.print_help()
        return 

    ############parse and load config file###############
    parse_config(CONF_FILE)

    ############init logging##############################
    init_logging(options.port)

    logging.info("Test info:Master start!")
    logging.error("Test error:Master start!")
    logging.debug("Test debug:Master start!")
    
    ############setting tornado server#####################
    global http_server

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    #################init db const value###################
    TableSelectSql(GlobalVar.get_db_handle())
    TableFields(GlobalVar.get_db_handle())

    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ############start tornado server#######################
    tornado.ioloop.IOLoop.instance().start()
    logging.info('Exit Master')

if __name__ == "__main__":
    main()
