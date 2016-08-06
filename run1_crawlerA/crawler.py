# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:10:58 2016

@author: xiaobei
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging.handlers
from rewritesummary import PushSummary
from Rest import REST
import json
from estimate_time import Time
from extension import search as sch
import logging
from process_profile import preprocess_profile
import time
from tweepy.api import API

consumer_key = "xhxmrGATSWgi8abAj3MA8nuRJ"
consumer_secret = "bMvBg9Y1sMTWgBn8FV8zRHm1DnpET5u8g06WjxBshpopVvFqW6"

access_token = "2910563640-AlY4JW3qanLy7OzfcRhvXjb09642fnHOoEPAglf"
access_token_secret = "JX8AxeYBFHgJRH9xpNFmf1pzgbmZq9BD5pDlpzSlNOMX7"
logging.basicConfig(level=logging.INFO)


class TweetListener(StreamListener):
    def __init__(self, api=None):
        super(TweetListener, self).__init__(api)
        self.logger = logging.getLogger('tweetlogger')

        # print('a')
        statusHandler = logging.handlers.TimedRotatingFileHandler('status.log', when='H', encoding='utf-8', utc=True)
        statusHandler.setLevel(logging.INFO)
        self.logger.addHandler(statusHandler)

        warningHandler = logging.handlers.TimedRotatingFileHandler('warning.log', when='H', encoding='utf-8', utc=True)
        warningHandler.setLevel(logging.WARN)
        self.logger.addHandler(warningHandler)
        logging.captureWarnings(True)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.WARN)
        self.logger.addHandler(consoleHandler)

        # self.logger.setLevel(logging.INFO)
        self.count = 0

    def on_data(self, data):
        data = json.loads(data, encoding='utf-8')
        # print(data)
        pushSummary.pushSummarys(data)
        self.count += 1
        # self.logger.info(data)
        # with open('test.txt','a') as f:
        #     f.write(data+'\n')
        # print(data)
        # tweet=json.load(data)
        # print(type(tweet))
        # pushSummary.pushSummarys(json.loads(data))
        # print(self.count)
        if self.count % 1000 == 0:
            print("%d statuses processed %s" % (self.count, time.strftime('%X', time.localtime(time.time()))))
        return True

    def on_error(self, exception):
        self.logger.warning(str(exception))


if __name__ == '__main__':
    # api = API(proxy='127.0.0.1:6666')

    listener = TweetListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    # clientid = rest.Getclientid()
    with open('clientidrun1.txt', 'r') as f:
        clientid = f.read()
    rest = REST(clientid)
    # topics = rest.GetTopic()
    # interest_files = {}
    # count = 0
    # x = 0
    # topicid = {}
    # for i in topics:
    #     number = i['topid']
    #     title = i['title']
    #     Desc = i['description']
    #     Narr = i['narrative']
    #     title = preprocess_profile(title)
    #     Desc = preprocess_profile(Desc)
    #     Narr = preprocess_profile(Narr)
    #     tf = {}
    #     for word in title:
    #         if word in tf:
    #             tf[word] += 1
    #         else:
    #             tf[word] = 1
    #     for word in Desc:
    #         if word in tf:
    #             tf[word] += 1
    #         else:
    #             tf[word] = 1
    #     for word in Narr:
    #         if word in tf:
    #             tf[word] += 1
    #         else:
    #             tf[word] = 1
    #     a = sorted(tf.items(), key=lambda d: d[1], reverse=True)
    #     b = [d[0] for d in a[0:5]]
    #     stemwords_interest_profile = b
    #     b = ' '.join(b)
    #     s = sch(b)
    #     count += 1
    #     logging.info(count)
    #     search = []
    #     stf = {}
    #     for i in s:
    #         j = preprocess_profile(i.title)
    #         for k in j:
    #             f = []
    #             for l in k:
    #                 if ord(l) < 127:
    #                     f.append(l)
    #             search.append(''.join(f))
    #     for word in search:
    #         if word in stf:
    #             stf[word] += 1
    #         else:
    #             stf[word] = 1
    #     d = sorted(stf.items(), key=lambda d: d[1], reverse=True)
    #     e = 0
    #     for n in range(len(d)):
    #         if d[n][0] not in stemwords_interest_profile:
    #             stemwords_interest_profile.append(d[n][0])
    #             e += 1
    #         if e >= 10:
    #             break
    #     interest_files[x] = stemwords_interest_profile
    #     topicid[x] = number
    #     x += 1
    with open('q_e.txt', 'r') as f:
        c = f.read()
    interest_files = eval(c)
    with open('q_x.txt', 'r') as ff:
        d = ff.read()
    topicid = eval(d)
    # with open('q_e.txt', 'w') as f:
    #     f.write(str(interest_files))
    # with open('q_x.txt', 'w') as ff:
    #     ff.write(str(topicid))
    times = Time('Tue Aug 02 00:00:00 +0000 2016')
    fa = open('A.txt', 'a', encoding='utf-8')
    pushSummary = PushSummary(0.9, interest_files, times, rest, fa, topicid)
    while True:
        try:
            stream.sample()
        except Exception as ex:
            print(str(ex))
        pass
