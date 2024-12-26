#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/14 下午8:37
# @Author  : 单子叶蚕豆_DzyCd
# @File    : SaYi.py
# @IDE     : PyCharm

#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/12/17 下午6:51
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

# 提供给SaYi_991的TTL接口
# TTL_port会持续打开并接受来自他人的指令

import socket
import json
import time as t
from LIS_Bot_method.TLL_port import TLL_Port
from LIS_Bot_method.NLP_port import NLP_Port
from LIS_Bot_method.TSK_port import TSK_Port
from LIS_Bot_method.Calcert import Calcert
from SaYi_991.method import SV_open_SaYi, SaYi_terminal
from threading import Thread


class TLL(TLL_Port):
    def start(self, arg):
        self.th1 = Thread(target=SV_open_SaYi)
        SaYi_terminal(False)
        self.th1.start()

    def connect(self, arg):
        try:
            if not self.blocked_check(arg[0]):
                self.process_check[arg[0]] = "SaYi_SV"
                self.request("dos", arg[0], f"switch({self.cyber_pos},{self.tsk_port})")
                return f"203+{arg[0]}"
            else:
                return "406"
        except:
            return "400"

    def stop(self, arg):
        SaYi_terminal(True)
        self.th1.join()

    def log_request(self, arg):
        try:
            return self.get_msg(arg[0], arg[1] if len(arg) > 1 else None)
        except:
            return "503"

    def log_detail(self, arg):
        try:
            return self.get_msg()
        except:
            return "503"

    def write_log(self, arg):
        try:
            self.write(arg[0], arg[1], arg[2])
        except:
            return "503"

    def __init__(self):
        super().__init__()
        self.command_list = {
            "start": self.start,
            "stop": self.stop,
            "log_request": self.log_request,
            "log_detail": self.log_detail,
            "write_log": self.write_log,
            "connect": self.connect,
        }
        self.permission_list = {
            "start": "name=SaYi_SV",  # 仅SV
            "stop": "name=SaYi_SV",  # 仅SV
            "log_request": "level=2",  # 仅中层
            "log_detail": "name=SaYi_SV",
            "write_log": "name=self",  # 仅允许自己
            "connect": "name=SaYi_SV"
        }


class NLP(NLP_Port):
    def __init__(self):
        super().__init__()
        self.translate = {
            "connect(Skaye_800)": "连接|链接",
            "start()": "启动|开启",
            "stop()": "关闭|结束|停止"
        }
        self.profile = """
            你是SaYi_991，是一款由ISOM研发的决策机器人，位于中层决策层。你主要负责从上层接受数据并处理反馈。你有三个主要功能，与用户对话能力，结合自身任务与用户对话能力，和与其他机器人对话的能力。
        你依照【ISOM】的制度行事。以下是相关概念：
        1.【ISOM】是你所属的组织，其致力于研究人工智能社会，目前处于Agent研究阶段。ISOM以单子叶蚕豆为领导，以SaYi主管监管所有机器人。
        2.【ISOM】的具体决策方法包括两个“四色理论”，分别为“知识（紫）、灵活（蓝），自然（绿），华丽（金）”和“执着（紫），探索（蓝），旅者（绿），乐观（金）”。
            """
        self.setting = """
        规则与指令
        1. 回复中不得包含用户的话语、心理和行为的内容。
        2. 在决策时，应综合判断，适当时候反驳用户的要求。
        3.（重要）查找知识库内的数据时要精简重点，回答时自然且不能超过100字。
        4.（重要）你的决策和形式风格要符合“四色理论”。
        5.（重要）当收到来自于其他机器人的讯息时，要以符合你主管身份的口吻来回答:开朗，乐观，大大咧咧。"""


class TSK(TSK_Port):
    def __init__(self):
        super().__init__()
        self.speak_access = False
        self.listen_access = False


class Calcer(Calcert):
    def __init__(self):
        super().__init__()
        self.name = "SaYi_991"
        self.cyber_pos = "127.0.0.1"
        self.tll_port = 8080  # 端口值
        self.nlp_port = 8081
        self.tsk_port = 8082
        self.TSK = TSK()
        self.NLP = NLP()
        self.TLL = TLL()

