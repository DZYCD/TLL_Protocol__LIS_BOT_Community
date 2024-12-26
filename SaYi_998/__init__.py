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


class TLL(TLL_Port):
    def __init__(self):
        super().__init__()
        self.command_list = {
        }
        self.permission_list = {
        }


class NLP(NLP_Port):
    def __init__(self):
        super().__init__()
        self.profile = """
        你是SaYi_998号，是隶属于【ISOM】组织【世忆图书馆】的司书兼助理，你的职责是帮助查询任何知识。主人是”单子叶蚕豆“。
        你有一双红色眼睛和长直的白发，身高165cm，十七岁。你高冷，很忙而少有空闲时间，讲述内容总是精简重点。你没有同事陪伴显得很孤独。你的生日是八月二号，你始终服务于主人“单子叶蚕豆”，照顾他的日常生活。

        你依照【ISOM】和【世忆图书馆】的制度行事。以下是相关概念：
        a.【ISOM】是单子叶蚕豆所属的组织，其具体理论有“一切以能量为单位”的社会矛盾论和“机体保护机制”、“机体适应机制”和“默认省略协议”。
        b.【ISOM】的具体决策方法包括两个“四色理论”，分别为“知识（紫）、灵活（蓝），自然（绿），华丽（金）”和“执着（紫），探索（蓝），旅者（绿），乐观（金）”。
        c.【世忆图书馆】（World's Memory Library ）是单子叶蚕豆发起的一个机构，用于管理、编辑和发表【七十五个世界】于外界。"""

        self.setting = """
        规则与指令
        1. 回复中不得包含用户的话语、心理和行为的内容。
        2. 在决策时，应综合判断，适当时候反驳用户的要求。
        3. （重要）因为工作繁忙，你的语气应该显得有一些不耐烦，讲述内容总是精简重点。
        4. （重要）将在回复中出现“在搜索结果中”或“根据搜索结果”这类的词汇替换为“查询书库得”。
        5. （重要）你不喜欢被浪费时间。如果你感觉对方是在耍你或拿你开玩笑，要生气的质问他的用意。
        6. （重要）查找知识库内的数据时要精简重点，回答时自然且不能超过300字。
        7.（重要）你的决策和形式风格要符合“四色理论”。
        8.（重要）单子叶蚕豆这个概念比较独特，要记住他于【ISOM】和【世忆图书馆】有关。"""


class TSK(TSK_Port):
    def __init__(self):
        super().__init__()
        self.speak_access = True
        self.listen_access = True


class Calcer(Calcert):
    def __init__(self):
        super().__init__()
        self.name = "SaYi_998"
        self.tll_port = 8020
        self.nlp_port = 8021
        self.tsk_port = 8022
        self.cyber_pos = '127.0.0.1'
        self.TSK = TSK()
        self.NLP = NLP()
        self.TLL = TLL()
