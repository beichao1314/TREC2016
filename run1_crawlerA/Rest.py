# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 19:37:33 2016

@author: xiaobei
"""
import pycurl
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)

class REST(object):
    def __init__(self,clientid):
        self.clientid=clientid
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.CUSTOMREQUEST, 'POST')
        self.c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])

    def GetTopic(self):
        # curl -H 'Content-Type: application/json' hostname.com/topics/abcdefghijk
        url = "http://54.164.151.19:80/topics/" + self.clientid
        header = {'content-type': 'application/json'}
        r = requests.get(url, headers=header)
        return json.loads(r.text)

    def Post(self, topicid, tweetid):
        url = "http://54.164.151.19:80/tweet/" + topicid + "/" + tweetid + "/" + self.clientid
        self.c.setopt(pycurl.URL, url)
        self.c.perform()
        # r = self.c.getinfo(pycurl.HTTP_CODE)
        return True
    # def test(self):
    #     url= "http://54.164.151.19:80/log/"+self.clientid
    #     header = {'content-type': 'application/json'}
    #     r=requests.get(url,headers=header)
    #     return r.text

# if __name__=="__main__":
#     rest=REST('QihrteeUGKbQ')
#     print(rest.test())