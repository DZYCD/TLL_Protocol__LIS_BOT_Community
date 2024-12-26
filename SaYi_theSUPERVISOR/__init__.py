#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/15 下午9:44
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

# 接口进入
from LIS_Bot_method.TLL_port import TLL_Port
from LIS_Bot_method.NLP_port import NLP_Port
from LIS_Bot_method.TSK_port import TSK_Port
from LIS_Bot_method.Calcert import Calcert
from threading import Thread
from .method import menu, SaYi_terminal


class TLL(TLL_Port):
    def start(self, arg):
        self.th1 = Thread(target=menu)
        SaYi_terminal(False)
        self.th1.start()

    def stop(self, arg):
        SaYi_terminal(True)
        self.th1.join()

    def get(self, arg):
        if arg[0] == 'access_list':
            return "202+" + f"dos+access_update({str(self.access_list)})"
        else:
            return "503"

    def __init__(self):
        super().__init__()
        self.access_list = {"DzyCd": {"level": 0, "cyber_pos": "None", "real_pos": "None", "tll_port": "None"},
                            "SaYi_SV": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8040},
                            "SaYi_991": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8080},
                            "Skaye_800": {"level": 3, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8060},
                            "SaYi_998": {"level": 2, "cyber_pos": '127.0.0.1', "real_pos": "None", "tll_port": 8020}}

        self.command_list = {
            "start": self.start,
            "stop": self.stop,
            "get": self.get,
            "give_output": self.give_output,
            "send": self.send
        }
        self.permission_list = {
            "start": "name=DzyCd",
            "stop": "name=DzyCd",
            "get": "",
            "give_output": "",
            "send": "name=SaYi_SV"
        }


class NLP(NLP_Port):
    def __init__(self):
        super().__init__()
        self.profile = """
            你是SaYi_SV，一般称呼为SaYi主管。你是一款由ISOM研发的主管机器人，位于中层决策层。你主要负责监管本公司生产设计的所有机器人。你有三个主要功能，与用户对话能力，结合自身任务与用户对话能力，和与其他机器人对话的能力。
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
        5.（重要）当收到来自于其他机器人的讯息时，要以符合你身份的口吻来回答:有爱，简单，综合。"""


class TSK(TSK_Port):
    def __init__(self):
        super().__init__()
        self.speak_access = False
        self.listen_access = False


class Calcer(Calcert):
    def __init__(self):
        super().__init__()
        self.name = "SaYi_SV"
        self.tll_port = 8040
        self.nlp_port = 8041
        self.tsk_port = 8042
        self.cyber_pos = '127.0.0.1'
        self.TSK = TSK()
        self.NLP = NLP()
        self.TLL = TLL()
