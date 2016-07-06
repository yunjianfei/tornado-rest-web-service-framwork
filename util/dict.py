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

Note: All type class use the ENUM structure, the type's value must start at 0, and sequential growth by 1

"""


class HostType:
    MASTER = 0
    DISPATHER = 1
    AGENT = 2
    MAX_TYPE = 3

    to_string = {
        MASTER: "Master",
        DISPATHER: "Dispather",
        AGENT: "Agent",
    }

    def check(self, hosttype):
        for i in range(0, HostType.MAX_TYPE):
            if hosttype == i:
                return True
        return False
