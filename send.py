#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/17 下午9:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : send.py
# @IDE     : PyCharm
import json

msg = "{'DzyCd':{'level':0,'cyber_pos':None,'real_pos':None,'ttl_port':None},'SaYi_SV':{'level':2,'cyber_pos':'127.0.0.1','real_pos':None,'ttl_port':8040},'SaYi_991':{'level':2,'cyber_pos':'127.0.0.1','real_pos':None,'ttl_port':8080},'Skaye_800':{'level':3,'cyber_pos':'127.0.0.1','real_pos':None,'ttl_port':8060}}"

msg = msg.replace("'", '"')
msg = msg.replace('None', '"None"')
print(msg[30:33])
json.loads(msg)
