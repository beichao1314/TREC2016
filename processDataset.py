# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:38:57 2016

@author: xiaobei
"""
import json
filepath='E:/TREC/realtime/dataset/twitter-json-scrape-2011-09/2011/09/27/19/48.json'
with open(filepath,'r') as f:
    data=f.readlines()
for item in data:
    #print(json.dumps(item))
    print(json.loads(item)['text'])
    print('________________________________________')
