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

import tornado.web
import json
import logging
import time
from util.config import Config
from util.dict import HostType 
from util.httpresponse import Response as Resp, ResponseCode as RespCode
from util import tools
from dao.host import HostDao


class HostHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.application.db
        self.host_dao = HostDao(self.db)
        self.Resp = Resp()
        self.HostType = HostType()

    def get(self):
        """
            The GET method is used to get one Host by hostname or host list
        """
        hostname = self.get_argument('hostname', None)
        host_id = self.get_argument('host_id', None)
        hostname = tools.strip_string(hostname)
        host_id = tools.to_int(host_id)

        resp = None 
        if hostname is not None:
            logging.info("In GET method! Get host by hostname: '%s'", str(hostname))
            host = self.host_dao.get_by_hostname(hostname)
            resp = host
        elif host_id is not None:
            logging.info("In GET method! Get host by host_id: '%s'", str(host_id))
            host = self.host_dao.get_by_id(host_id)
            resp = host
        else:
            logging.info("In GET method! Get all hosts.")
            hosts = self.host_dao.get_all()
            resp = hosts

        logging.info("Query result: %s", str(resp))

        if resp is None or len(resp) == 0:
            logging.error("There is no record! ")
            resp = self.Resp.make_response(code=RespCode.NO_RECORD)
            self.write(resp)
            return

        resp = self.Resp.make_response(code=RespCode.SUCCESS, content=resp)
        self.write(resp)

    def post(self):
        """
            The POST method is used to inert one host into 'Host' Table
        """
        data = self.request.body
        h = json.loads(data)

        logging.info("In POST method. Receive data: %s", str(data))
        
        # start check parameters
        hostname = h.get('hostname', None)
        hostname = tools.strip_string(hostname)
        if hostname is None:
            logging.error("There is no parameter 'hostname'! ")
            resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='hostname')
            self.write(resp)
            return

        ip = h.get('ip', None)
        ip = tools.strip_string(ip)
        if ip is None:
            logging.error("There is no parameter 'ip'! ")
            resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='ip')
            self.write(resp)
            return

        # check if exist
        if_exist = self.host_dao.if_exist(hostname, ip)
        if if_exist is True:
            logging.error("The host has existed!")
            resp = self.Resp.make_response(code=RespCode.HAS_EXISTED, para='Host')
            self.write(resp)
            return

        host_type = tools.to_int(h.get('host_type', 0))
        if host_type is None or self.HostType.check(host_type) != True:
            logging.error("The value of parameter 'host_type' is invalid!")
            resp = self.Resp.make_response(code=RespCode.INVALID_PARAMETER, para='host_type')
            self.write(resp)
            return

        cpu_count = tools.to_int(h.get('cpu_count', 8))
        memory = tools.to_int(h.get('memory', 8))
        os = h.get('os', '')
        comment = h.get('comment', '')

        worker_num = tools.to_int(h.get('worker_num', 0))
        if worker_num is None or worker_num == 0:
            worker_num = Config.default_worker_num

        logging.debug("Check parameters complete, ready to save in db")

        # save in db
        host = dict()
        host['hostname'] = hostname
        host['host_type'] = host_type
        host['ip'] = ip
        host['cpu_count'] = cpu_count
        host['memory'] = memory
        host['os'] = os
        host['comment'] = comment
        host['worker_num'] = worker_num
        create_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        host['create_time'] = create_time

        ret = self.host_dao.insert_by_dict(host)
        if ret is None:
            err_str = "Error oucurred when insert into table 'Host'"
            logging.error(err_str)
            resp = self.Resp.make_response(code=RespCode.DB_ERROR, err_str=err_str)
            self.write(resp)
            return

        logging.info("Save host object successed! The host: %s", str(host))

        host['host_id'] = ret
        resp = self.Resp.make_response(code=RespCode.SUCCESS, content=host)
        self.write(resp)

    def put(self):
        """
            The put method is used to modify the Host's worker_num
        """
        data = self.request.body
        h = json.loads(data)

        logging.info("In PUT method! Receive data: %s", str(data))
        
        # start check parameters
        hostname = h.get('hostname', None)
        host_id = h.get('host_id', None)
        hostname = tools.strip_string(hostname)
        host_id = tools.to_int(host_id)

        worker_num = tools.to_int(h.get('worker_num', 0))
        if worker_num is None or worker_num == 0:
            logging.error("There is no parameter 'worker_num'! ")
            resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='worker_num')
            self.write(resp)
            return

        if hostname is not None:
            ret = self.host_dao.update_worker_num_by_hostname(hostname, worker_num)
            err_str = "Error oucurred when Update host by hostname '%s', worker_num: %s" % (hostname, str(worker_num))
            host = self.host_dao.get_by_hostname(hostname)
        elif host_id is not None:
            ret = self.host_dao.update_worker_num_by_id(host_id, worker_num)
            err_str = "Error oucurred when Update host by host_id '%s', worker_num: %s" % (str(host_id), str(worker_num))
            host = self.host_dao.get_by_id(host_id)
        else:
            logging.error("There is no parameter 'hostname' or 'host_id'! ")
            resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='hostname or host_id')
            self.write(resp)
            return

        if ret is None:
            logging.error(err_str)
            resp = self.Resp.make_response(code=RespCode.DB_ERROR, err_str=err_str)
            self.write(resp)
            return

        if host is None:
            logging.info("No record!")
            resp = self.Resp.make_response(code=RespCode.NO_RECORD)
            self.write(resp)
            return

        logging.info("Update host object successed!")
        resp = self.Resp.make_response(code=RespCode.SUCCESS, content=host)
        self.write(resp)

    def delete(self):
        """
            The DELETE method is used to delete Host object
        """
        hostname = self.get_argument('hostname', None)
        host_id = self.get_argument('host_id', None)
        hostname = tools.strip_string(hostname)
        host_id = tools.to_int(host_id)

        if hostname is not None:
            logging.info("In DELETE method! Delete host by hostname: '%s'.", str(hostname))
            ret = self.host_dao.del_by_hostname(hostname)
            err_str = "Error oucurred when Delete host by hostname: '%s'" % hostname
        elif host_id is not None:
            logging.info("In DELETE method! Delete host by host_id: '%s'.", str(host_id))
            ret = self.host_dao.del_by_id(host_id)
            err_str = "Error oucurred when Delete host by host_id: '%s'" % str(host_id)
        else:
            logging.error("There is no parameter 'hostname' or 'host_id'! ")
            resp = self.Resp.make_response(code=RespCode.NO_PARAMETER, para='hostname or host_id')
            self.write(resp)
            return
        
        if ret is None:
            logging.error(err_str)
            resp = self.Resp.make_response(code=RespCode.INVALID_PARAMETER, err_str=err_str)
            self.write(resp)
            return

        logging.info("Delete host object successed!")

        resp = self.Resp.make_response(code=RespCode.SUCCESS)
        self.write(resp)
