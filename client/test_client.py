#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   Test db
#

import time,signal,logging,os
import urllib
import urllib2
import tornado.httpclient
import tornado
import json
from tornado.httpclient import AsyncHTTPClient

def make_qs(query_args):
    kv_pairs = []
    for (key, val) in query_args.iteritems():
        if val:
            if isinstance(val, list):
                for v in val:
                    kv_pairs.append((key, v))
            else:
                kv_pairs.append((key, val))

    qs = urllib.urlencode(kv_pairs)

    return qs

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.info('Will shutdown in %s seconds ...', 2)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + 2

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logging.info('Shutdown')
    stop_loop()

    
def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print "-----------------------------------------------------------------"
        print "Request Url: " + response.request.url
        print "\nMethod: " + response.request.method
        if response.request.body:
            print "\nRequest Body: \n" + json.dumps(json.loads(response.request.body), indent=2)

        print "\nResponse: "
        body =  response.body
        resp = json.loads(body) 
        print json.dumps(resp, indent=2)

    #tornado.ioloop.IOLoop.instance().stop()

def test_host(http_client):
    host = {}
    host['hostname'] = "test9"
    host['ip'] = '192.168.10.47'
    host['worker_num'] = 29
    host['host_id'] = '4'

    #test add
    url = "http://192.168.10.47:9999/host"
    http_client.fetch(url, handle_request, method='POST', body=json.dumps(host))

    #TODO
    #test modify
    #url = "http://192.168.10.47:9999/host"
    #http_client.fetch(url, handle_request, method='PUT', body=json.dumps(host))

    ##test delete 
    #url = "http://192.168.10.47:9999/host?hostname='test'"
    #url = "http://192.168.10.47:9999/host?host_id=6"
    #http_client.fetch(url, handle_request, method='DELETE')

    ##test get 
    url = "http://192.168.10.47:9999/host"
    #url = "http://192.168.10.47:9999/host?hostname='test3'"
    #url = "http://192.168.10.47:9999/host?host_id='100'"
    http_client.fetch(url, handle_request, method='GET')

def main():
    ##############set signal handler#######################
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    http_client = AsyncHTTPClient()

    test_host(http_client)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
