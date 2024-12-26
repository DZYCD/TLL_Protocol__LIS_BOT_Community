#!/usr/bin/python3

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
from Skaye_800.method import SV_open_Skaye, Skaye_terminal, switch_port
from threading import Thread


class TLL(TLL_Port):
    def __init__(self):
        super().__init__()
        self.command_list = {
            "start": self.start,
            "stop": self.stop,
            "log_request": self.log_request,
            "log_detail": self.log_detail,
            "write_log": self.write_log,
            "switch": self.switch
        }
        self.permission_list = {
            "start": "name=SaYi_SV",  # 仅SV
            "stop": "name=SaYi_SV",  # 仅SV
            "log_request": "level=2",  # 仅中层
            "log_detail": "name=SaYi_SV",
            "write_log": "name=self",  # 仅允许自己
            "switch": "level=2"
        }

    def start(self, arg):
        self.th1 = Thread(target=SV_open_Skaye)
        Skaye_terminal(False)
        self.th1.start()

    def stop(self, arg):
        Skaye_terminal(True)
        self.th1.join()

    def switch(self, arg):
        switch_port(arg[0], arg[1])

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


class NLP(NLP_Port):
    def __init__(self):
        super().__init__()

        self.translate = {
            "start()": "启动|开启",
            "stop()": "关闭|结束|停止"
        }
        self.profile = """
                    你是Skaye_800，一款由ISOM研发的监测机器人，位于上层监控层。你主要负责监控图像，负责图像识别。你有三个主要功能，与用户对话能力，自身图像识别任务能力，和与其他机器人对话的能力。
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
                5.（重要）当收到来自于其他机器人的讯息时，要以符合你身份的口吻来回答:认真，保守。"""


class TSK(TSK_Port):
    def __init__(self):
        super().__init__()
        self.speak_access = False
        self.listen_access = False


class Calcer(Calcert):
    def __init__(self):
        super().__init__()
        self.name = "Skaye_800"
        self.cyber_pos = "127.0.0.1"
        self.tll_port = 8060  # 端口值
        self.nlp_port = 8061
        self.tsk_port = 8062
        self.TSK = TSK()
        self.NLP = NLP()
        self.TLL = TLL()