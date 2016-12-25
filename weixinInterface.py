# -*- coding: utf-8 -*-
import hashlib
import web
import time
import os
import urllib2,json
from lxml import etree


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)  # get current path
        self.templates_root = os.path.join(self.app_root, 'templates')  # get the path of templates
        self.render = web.template.render(self.templates_root)  # apply template

    def GET(self):  # get input parameter
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "york"  # token,input by yourself, sina must be the same as wechat
        list = [token, timestamp, nonce]  # 字典序排序
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()  # sha1加密算法

        if hashcode == signature:  # 如果是来自微信的请求，则回复echostr
            return echostr

    def POST(self):
        str_xml = web.data()  # get data from post
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msg_type = xml.find("MsgType").text
        from_user = xml.find("FromUserName").text
        to_user = xml.find("ToUserName").text
        if msg_type == 'event':
            if xml.find("Event").text == 'subscribe':
                return self.render.reply_text(from_user, to_user, int(time.time()), "Thank you for subscribing!")
        if msg_type == 'text':
            content = xml.find("Content").text
            if content[0:2] == '快递':
                return self.render.reply_text(from_user, to_user, int(time.time()), "copy that")
                # post = str(content[2:])
                # query = urllib2.urlopen('http://www.kuaidi100.com/autonumber/autoComNum?text='+post)
                # # 883884431991145739
                # h = query.read
                # k = eval(h)
                # result = k["auto"][0]['comCode']
                # return self.render.reply_text(from_user,to_user,int(time.time()), result)
            elif content == 'help':
                return self.render.reply_text(from_user, to_user, int(time.time()), "随便看看？（对不起我功能有限QAQ）")
            else:
                return self.render.reply_text(from_user, to_user, int(time.time()), content)
