#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/17 下午6:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import socket
import time

# NLP 用于对自然语言转写TTL并提供聊天机制
class NLP_Port:
    def __init__(self):
        self.name = "LIS_BOT"
        self.function = ["用自己的语言陈述下面的处理结果:", ""]
        self.status = "finish"
        self.profile = """
        你是LIS_BOT，是一款由ISOM研发的机器人。你有三个主要功能，与用户对话能力，结合自身任务与用户对话能力，和与其他机器人对话的能力。
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
"""
        self.local_TLL = ""
        self.cyber_pos = "127.0.0.1"
        self.real_pos = ""
        self.nlp_port = None
        self.tll_port = None
        self.tsk_port = None
        self.socket = ""
        self.vocal_output = False
        self.history_list = []
        self.round = 0
        self.translate = {
            "open()": "desc"
        }
        self.spark = ChatSparkLLM(spark_api_url='wss://spark-api.xf-yun.com/v3.5/chat',
                                  spark_app_id='bdf37372',
                                  spark_api_key='d0d90bd21e1eb0ad2c116928e38ad72b',
                                  spark_api_secret='NGFkYTBmYWQxMDM0MGUxZWE0ZjlkZjdi',
                                  spark_llm_domain='generalv3.5',
                                  streaming=False)



    def get_process(self, msg, mode):
        # mode0 : 碎片信息转写（涉及Natual to TLL、TLL to Natual时使用) mode1：正常聊天
        message = self.function[mode] + msg

        messages = [
            ChatMessage(role="system", content=self.profile),
            ChatMessage(role="system", content=self.setting),
        ]
        s = 0
        for i in self.history_list:
            messages.append(ChatMessage(role="user" if s % 2 == 0 else "assistant", content=i))
            s += 1

        messages.append(ChatMessage(role="user", content=message))
        handler = ChunkPrintHandler()

        a = self.spark.generate([messages], callbacks=[handler])
        p = a.dict()

        token_count = p["llm_output"]["token_usage"]
        p = p["generations"][0][0]["text"]

        self.history_list.append(msg)
        self.history_list.append(p)

        if token_count["total_tokens"] > 1200:
            self.round = self.round // 2 - (self.round % 2)
        else:
            self.round = self.round + 2

        while len(self.history_list) > self.round:
            del self.history_list[0]

        return p

    # 语言转述
    def central_Split(self, msg):
        process_result = "正在执行" if self.status == "finish" else self.status
        return msg + "结果为" + process_result

    # 提炼号的关键词在确认为TLL时进行TLL处理
    def TLL_to_Natual(self, msg):
        if "finish" == msg[0:6]:
            msg = msg[6:]
        bot_name, command, target_name, func, time, place = msg.split(" ")
        time = float(time)
        body, args = func.split('(')
        arg, ans = args.split(')')
        cyber_pos, port, real_pos = place.split('+')
        msg = f"{bot_name} 说 {arg}"
        return msg

    # 外面返回的TLL在确认陈述给人时进行Natual处理
    def Natual_to_TLL(self, msg):
        text = "在这句话中，提取出来和被要求一方的名字、被要求的功能，以“【被要求的一方名字】+【被要求的功能】”格式返回，中间要有一个加号，不要有其他文字："
        messages = [ChatMessage(role="user", content=text + msg)]
        handler = ChunkPrintHandler()

        a = self.spark.generate([messages], callbacks=[handler])
        p = a.dict()
        # print(p["generations"][0][0]["text"])
        p = p["generations"][0][0]["text"].replace("【", "").replace("】", "")
        botname, command = p.split('+')

        return f"{self.name} dos {self.name} send({botname},{command}) {time.time()} {self.cyber_pos}+{self.tll_port}+{self.real_pos}"

    def receiver_judge(self, msg, language):
        if language == "TLL":
            return "Natual" if "finish" == msg[0:6] else "TLL"

        text = "判断这句话是不是在要求你命令别人。如果是，只返回“TLL”，否则只返回“Natual”，不要带有多余内容:"
        # print(text+msg)
        messages = [ChatMessage(role="user", content=text + msg)]
        handler = ChunkPrintHandler()
        a = self.spark.generate([messages], callbacks=[handler])
        # print(text + msg)
        p = a.dict()
        return p["generations"][0][0]["text"]

    # 确定语言类型
    def language_judge(self, msg):
        try:
            bot_name, command, target_name, func, time, place = msg.split(" ")
            # time = float(time)
            # body, args = func.split('(')
            # arg, ans = args.split(')')
            # cyber_pos, port, real_pos = place.split('+')
            if command not in ["cons", "tips", "dos"]:
                return "Natual"
            return "TLL"
        except:
            return "Natual"

    def tell_to_port(self, msg):
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.nlp_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()

    def tell_to_TSK(self, msg):
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.tsk_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()

    # 上传给自己的TLL端口
    def tell_to_TLL(self, msg):
        bot_name, command, target_name, func, time, place = msg.split(" ")
        if func.split('(')[0] == 'dec_':
            func = "None()"
            for i in self.translate.items():
                key, v = i[0], i[1].split('|')
                for value in v:
                    if value in msg:
                        func = key
                        break
                if func == key:
                    break

        msg = f"process{bot_name} {command} {target_name} {func} {time} {place}"
        # print(self.tll_port)
        socket_client = socket.socket()
        socket_client.connect((self.cyber_pos, self.tll_port))
        socket_client.send(msg.encode("utf-8"))
        socket_client.close()
        # print("send back:"+msg)

    # 上传给外部控制台
    def tell_to_Natual(self, msg):
        return msg

    def decode(self, msg):
        language = self.language_judge(msg)
        receiver = self.receiver_judge(msg, language)
        # print(language, receiver)
        # 释放截获信号
        if language == "TLL":
            if receiver == "Natual":
                msg = self.TLL_to_Natual(msg)
                return msg
            else:
                self.tell_to_TLL(msg)
        else:
            if receiver == "Natual":
                msg = self.get_process(msg, 1)
                return self.tell_to_Natual(msg)
            else:
                self.tell_to_TLL(self.Natual_to_TLL(msg))
                # self.tell_to_Natual(self.central_Split(msg))

    def boot(self):
        self.socket = socket.socket()
        print(self.name + ": NLP open in ", self.cyber_pos, self.nlp_port)
        self.socket.bind((self.cyber_pos, self.nlp_port))
        self.socket.listen(5)

        while True:
            conn, address = self.socket.accept()
            data: str = conn.recv(1024).decode("UTF-8")
            # print("get message:" + data)
            if len(data):
                try:
                    ans = self.decode(data)
                    if ans is not None:
                        self.tell_to_TSK("speak"+ans)
                except Exception as e:
                    print(f"\033[0;31m[!]From NLP:{e}\033[0m")
            conn.close()
