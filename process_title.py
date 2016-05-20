# -*- coding: utf-8 -*-
"""
Created on Sun May 15 12:17:38 2016

@author: xiaobei
"""
import xml.etree.ElementTree as ET 
import nltk
from nltk.corpus import stopwords

def removeStopWords_1(originSegs):
    stops = set(stopwords.words('english'))
    resultStr = []
    for seg in originSegs:
        seg = seg.lower()
        if seg not in stops  and seg.isalpha():
            resultStr.append(seg)
            #print resultStr
    return resultStr
    
filepath_interest_profile='E:/TREC/interest_profile.xml'
tree = ET.parse(filepath_interest_profile)
#print(tree)
rootr = tree.getroot()
#print(rootr)
for i in rootr:
    number=i.find('Number').text
    #print(number)
    title=i.find('title').text
    #print(title)
    titlewords=nltk.word_tokenize(title)
    removeStopWords=removeStopWords_1(titlewords)
    #print(removeStopWords)