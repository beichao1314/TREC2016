# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:14:57 2016

@author: xiaobei
"""
import json
import bz2file
filepath='F:/twitter/07/20/00/30.json.bz2'
with bz2file.open(filepath,'r') as f:
    for line in f: 
        #line=str(line)
        line=str(line, encoding = "utf-8")
        if line[:10]=='{"delete":':
            continue
        #print(line)
        tweet=json.loads(line)
        print(tweet['id'])
        print(tweet['lang'])
        #print(tweet['text'])
        #print(tweet['created_at'])
        print(tweet['favorite_count'])
        print(tweet['retweet_count'])
        #print(tweet['user'])
        #print(tweet['entities'])
