# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 16:17:49 2016

@author: xiaobei
"""

import nltk
from nltk.corpus import stopwords
import re


def removeStopWords_1(originSegs):
    stops = set(stopwords.words('english'))
    resultStr = [seg.lower() for seg in originSegs if seg.lower() not in stops and seg.isalpha()]
    return resultStr


def filters(content):
    results = re.compile(r'http://[a-zA-Z0-9.?/&=:]*', re.S)
    filter = results.sub("", content)
    return filter


def preprocess_profile(sentence):
    # filterwords = filters(sentence)
    words = nltk.word_tokenize(sentence)
    removestopwords = removeStopWords_1(words)
    result = stemword(removestopwords)
    return result


def stemword(word):
    porter = nltk.PorterStemmer().stem
    result = list(map(porter, word))
    return result
