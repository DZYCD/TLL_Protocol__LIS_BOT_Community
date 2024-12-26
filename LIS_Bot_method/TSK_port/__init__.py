#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved 
#
# @Time    : 2024/12/17 下午6:54
# @Author  : 单子叶蚕豆_DzyCd
# @File    : __init__.py.py
# @IDE     : PyCharm

import numpy as np
import os
import time
import pyaudio
import wave
from aip import AipSpeech
from playsound import playsound
import socket

class Wake_Up:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY, file_path, speak_path):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.file_path = file_path
        self.speak_path = speak_path

    def Read_msg(self, msg):
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        s = msg
        result = client.synthesis(s, 'zh', 1, {  # zh代表中文
            'vol': 5, 'per': 111
        })
        # 返回的是一个音频流，需要保存成mp3文件
        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if not isinstance(result, dict):
            with open(self.file_path, 'wb') as f:  # 创建mp3文件并具有写权限，用二进制的方式打开
                f.write(result)
        time.sleep(0.5)
        playsound(self.file_path)

    def record_sound(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        mindb = 7000  # 最小声音，大于则开始录音，否则结束
        delayTime = 1.3  # 小声1.3秒后自动终止
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        # snowboydecoder.play_audio_file()
        #print("开始!计时")

        frames = []
        flag = False  # 开始录音节点
        stat = True  # 判断是否继续录音
        stat2 = False  # 判断声音小了

        tempnum = 0  # tempnum、tempnum2、tempnum3为时间
        tempnum2 = 0

        while stat:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            audio_data = np.frombuffer(data, dtype=np.short)
            temp = np.max(audio_data)
            if temp > mindb and flag == False:
                flag = True
                print("开始录音>>>", end="")
                tempnum2 = tempnum

            if flag:
                if temp < mindb and stat2 == False:
                    stat2 = True
                    tempnum2 = tempnum

                if temp > mindb:
                    stat2 = False
                    tempnum2 = tempnum
                    # 刷新

                if tempnum > tempnum2 + delayTime * 15 and stat2 == True:
                    # print("间隔%.2lfs后开始检测是否还是小声" % delayTime)
                    if stat2 and temp < mindb:
                        stat = False
                        # 还是小声，则stat=True
                        # print("小声！")
                    else:
                        stat2 = False
                        # print("大声！")
            tempnum += 1
            # print(tempnum, tempnum2 + delayTime * 15)
        print("录音结束>>>", end="")

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def voice2text(self):
        # 语音转文本
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        ret = client.asr(self.get_data(), 'pcm', 16000, {'dev_pid': 1536}, )
        # print(ret)
        if ret['err_msg'] == 'recognition error.':
            result = ''
            return result
        else:
            result = ret['result']
            return result

    def get_data(self):
        # 读取语音
        with open(self.file_path, 'rb') as fp:
            return fp.read()

    def del_file(self):
        file_name = self.file_path
        try:
            os.remove(file_name)
            # print(f"Successful deleted {file_name}")
            f = open(file_name, mode="w")  # 音频-图片-视频  mode="wb"
            f.close()
            # print(f"Successful maked {file_name}")

        except FileNotFoundError:
            print(f"{file_name} not found")

    def Run_Talk(self):
        while True:
            time.sleep(5)

            self.record_sound()

            chat_message = self.voice2text()
            print("处理结果>>>", chat_message)

            self.del_file()
            if len(chat_message) > 0:
                return chat_message[0]


class TSK_Port:
    def __init__(self):
        self.TLL =None
        self.NLP = None
        self.name = None
        self.tsk_port = None
        self.cyber_pos = None
        self.APP_ID = ''
        self.API_KEY = 'G'
        self.SECRET_KEY = 'ag5'
        self.file_path = ".\\chat-audio.mp3"
        self.speak_path = ".\\res-audio.mp3"
        self.wk = Wake_Up(self.APP_ID, self.API_KEY, self.SECRET_KEY, self.file_path, self.speak_path)
        self.socket = socket.socket()
        self.listen_access = False
        self.speak_access = False

    def speak(self):
        while True:
            print(self.name + ": TSK open in ", self.cyber_pos, self.tsk_port)
            self.socket.bind((self.cyber_pos, self.tsk_port))
            self.socket.listen(1)

            while True:
                conn, address = self.socket.accept()
                data: str = conn.recv(1024).decode("UTF-8")
                # print("get message:" + data)
                if len(data):
                    try:
                        # print("get:" + data)
                        if data[0:5] == "speak":
                            data = data[5:]
                            if self.speak_access:
                                self.wk.Read_msg(data)
                            print(f'\033[33m{data}\033[0m')

                    except Exception as e:
                        print(f"\033[0;31m[!]From NLP:{e}\033[0m")
                conn.close()

    def user_input(self):
        with open(self.file_path, 'w'):
            pass
        with open(self.speak_path, 'w'):
            pass

        print("\033[0;32m[->] TSK启用录音功能\033[0m" if self.listen_access else "\033[0;31m[->] TSK禁用录音功能\033[0m")
        print("\033[0;32m[->] TSK启用语音功能\033[0m" if self.speak_access else "\033[0;31m[->] TSK禁用语音功能\033[0m")

        while True:
            try:
                if self.listen_access:
                    name = self.wk.Run_Talk()
                    # print(name)
                else:
                    name = input()

                if name[0:3] == "TLL":
                    command, target, function = name[4:].split(' ')
                    self.TLL.request(command, target, function)
                else:
                    self.NLP.tell_to_port(name)
            except Exception as e:
                print(f"\033[0;31m[!]From TSK:{e}\033[0m")

    def boot(self):
        from threading import Thread
        th2 = Thread(target=self.speak)
        th3 = Thread(target=self.user_input)

        th2.start()
        th3.start()

        th2.join()
        th3.join()


