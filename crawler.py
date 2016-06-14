# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:26:53 2016

@author: xiaobei
"""

import tweepy
from tweepy import OAuthHandler
import json
import bz2file

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("status:"+status.text)
    def on_data(self,raw_data):
        data = json.loads(raw_data)
        if 'delete' in data:
            pass
        d=dict(data)
        #if len(d.keys())!=1:
        print(type(data))
        #print(len(d.keys()))
        pass
    
        
consumer_key="LVKmQgPwlxnDYkEgIUYyvJ1q3"
consumer_secret="EDzft1TESd8huGgKJt5pvj1TzDOdHqsbdf1zF8MAcd1hrqQbI6"

access_token="2910563640-7Aer9hentGM4P43b8CZF8dDnwqH9V3Q2XETJSAr"
access_token_secret="iYBCfLs3TUT7Yl54ftJoYLuM81Mupy2SbshRBs4N9ffLA"

auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
#api = tweepy.API(auth, proxy='23.83.235.65:NDljMmVhNT@127.0.0.1:1080')
api = tweepy.API(auth)
#api = tweepy.API(auth,proxy="")
filepath='E:/TREC/TREC2015-tweetids.txt.bz2'
#print(api.get_status(622582311184306176))
"""with bz2file.open(filepath,'r') as fr:
    #print(type(lines))
    for line in fr:
        strs=str(line,encoding='utf-8')   
        #print(strs)
        #print(strs.strip('\n'))
        try:
            fw=open('E:/TREC/TREC2015-tweet.txt','a') 
            tweet=api.get_status(int(strs))
            print('complete:'+ strs)
            fw.write(str(tweet)+'\n')
            fw.close()
            #print(tweet)
        except:
            print('except:')
            
        """     
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#myStream.filter(track=['python'])
myStream.sample()