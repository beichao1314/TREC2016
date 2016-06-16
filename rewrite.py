# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 15:56:46 2016

@author: xiaobei
"""

import json
import bz2file
import os
import math
import xml.etree.ElementTree as ET 
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn  
import xml.dom.minidom
import re
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer  
import time
import tweepy
from tweepy import OAuthHandler
import json
import bz2file
import pymysql

def removeStopWords_2(originSegs):
    stops = set(stopwords.words('english'))
    resultStr = ''
    for seg in originSegs:
        seg = seg.lower()
        if seg not in stops  and seg.isalpha():
            resultStr+=seg+' '
            #print resultStr
    return resultStr 
    
def removeStopWords_1(originSegs):
    stops = set(stopwords.words('english'))
    resultStr = []
    for seg in originSegs:
        seg = seg.lower()
        if seg not in stops  and seg.isalpha():
            resultStr.append(seg)
            #print resultStr
    return resultStr
    
def StemWords(cleanWordsList):  
    stemWords=[]  
    for words in cleanWordsList: 
        #print(words)
        stemword=wn.morphy(words)
        if stemword==None:
            stemword=words
        stemWords.append(stemword)
        #print(wn.morphy(words))
        #print(stemWords)
    return stemWords 
    
def filters(words):
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    filterwords=[]    
    for word in words:
        if not(word in english_punctuations):
            filterwords.append(word)
    return filterwords
    
def calTheta(words, stream):
    theta={}
    lenOfWords=float(len(words))
    lenOfStream=0
    stream_words=[]
    for sentence in stream:
        word=nltk.word_tokenize(sentence)
        lenOfStream+=len(word)
        stream_words.append(word)
    for word in words:
        numOfWordInStream=0.0
        numOfWordInWords=float(words.count(word))
        Pt=numOfWordInWords/lenOfWords
        for words in stream_words:
            numOfWordInStream+=words.count(word)
        Ps=numOfWordInWords/float(numOfWordInStream)
        theta[word]=0.9*Pt+0.1*Ps
    return theta

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("status:"+status.text)
    def on_data(self,raw_data):
        data = json.loads(raw_data)
        d=dict(data)
        if len(d.keys())!=1:
            #print(data['text'])
            numberOfStream+=1
            pushSummary(data)
        #print(len(d.keys()))
        
        #print(data)
        #print('_________________________________________')
        pass
    
def preprocess(sentence):
    words=nltk.word_tokenize(sentence)
    filterwords=filters(words)
    removestopwords=removeStopWords_1(filterwords)
    stemwords=StemWords(removestopwords)
    return stemwords

#def Sql(sql,)
    
def pushSummary(tweet):
    
    filepath_interest_profile='E:/TREC/interest_profile.xml'
    tree = ET.parse(filepath_interest_profile)
    #print(tree)
    rootr = tree.getroot()
    for interest_file in rootr:
        wordInTweet={}
        numOfTweetOccurs={}
        numOfWord=0
        tfidf={}
        number=interest_file.find('Number').text
        #print(number)
        title=interest_file.find('title').text
        #print(title)
        stemwords_interest_profile=preprocess(title)
        if 'retweeted_status' in tweet:
            content=tweet['retweeted_status']['text']
            #print(tweet['id'])
        else:
            content=tweet['text']
        results=re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
        content=results.sub("",content)
        stemwords_tweet=preprocess(content)
        if tweet['lang']!='en':
            pass
        else:
            count=0
            for wordsss in stemwords_interest_profile:
                if wordsss in stemwords_tweet:
                    count+=1
            if count>=2:
                numOfWord+=len(stemwords_tweet)
                SumOfLenthOfStream+=numOfWord
                for word in stemwords_tweet:
                    if word in wordInTweet:
                        wordInTweet[word]+=1
                    else:
                        wordInTweet[word]=1
                    if word in wordInStream:
                        wordInStream[word]+=1
                    else:
                        wordInStream[word]=1
                    if word not in numOfTweetOccurs:
                        numOfTweetOccurs[word]=1
                    
                if cur.execute('select 1 from queries where query=(%s) limit 1',(number))==1:
                    cur.execute('select numOfWord from queries where query=(%s)',(number))
                    conn.commit()
                    numOfWord+=cur.fetchone()
                    cur.execute('update queries set numOfWord=(%s) where query=(%s)',(numOfWord,number))
                    conn.commit()
                    cur.execute('select numOfTweet from queries where query=(%s)',(number))
                    numOfTweet=cur.fetchone()+1
                    conn.commit()
                    cur.execute('updata queries set numOfTweet=(%s) where query=(%s)',(numOfTweet,number))
                    conn.commit()
                else:
                    cur.execute('insert into queries(query,numOfWord,numOfTweet) values(%s,%s,%s)',(number,numOfWord,1))
                    conn.commit()
                for word in wordInTweet:
                    if cur.execute('select 1 from word_query where word=(%s) and query=(%s)',(word,number))==1:
                        cur.execute('select tf from word_query where word=(%s) and query=(%s)',(word,number))
                        conn.commit()
                        tf=cur.fetchone()+wordInTweet[word]
                        cur.execute('update word_query set tf=(%s) where word=(%s) and query=(%s)',(tf,word,number))
                        conn.commit()
                    else:
                        cur.execute('inset into word_query(word,query,tf,numOfTweetOccurs) values(%s,%s,%s)',(word,number,1,0))
                        conn.commit()
                for word in numOfTweetOccurs:
                    if cur.execute('select 1 from word_query where word=(%s) and query=(%s)',(word,number))==1:
                        cur.execute('select numOfTweetOccurs from word_query where word=(%s) and query=(%s)',(word,number))
                        conn.commit()
                        num=cur.fetchone()
                        cur.execute('update word_query set numOfTweetOccurs=(%s) where word=(%s) and query=(%s)',(num+1,word,number))
                        conn.commit()
                        
            else:
                for word in stemwords_tweet:
                    if word in wordInStream:
                        wordInStream[word]+=1
                    else:
                        wordInStream[word]=1
            for word in stemwords_tweet:
                if word in word_timestamp:
                    deta=word_timestamp[word]-float(tweet['timestamp'])
                    if deta < 7200000:
                        decay=((float(deta-3600000.0))/3600000.0)*((float(deta-3600000.0))/3600000.0)
                        word_decay[word]=decay
                        word_timestamp[word]=float(tweet['timestamp_ms'])
                    else:
                        word_decay[word]=1
                else:
                    word_timestamp[word]=float(tweet['timestamp'])
                    word_decay[word]=1
            if count>=2:
                for word in stemwords_tweet:
                    cur.execute('select tf from word_query where word=(%s) and query=(%s)',(word,number))
                    conn.commit()
                    numofword=cur.fetchone()
                    cur.execute('select numOfWord from queries where query=(%s)',number)
                    conn.commit()
                    numofwordinall=cur.fetch()
                    tf=float(numofword)/float(numofwordinall)
                    cur.execute('select numOfTweet from queries where query=(%s)',number)
                    conn.commit()
                    numoftweet=cur.fetch()
                    cur.execute('select numOfTweetOccurs from word_query where word=(%s) and query=(%s)',(word,number))
                    conn.commit()
                    numoftweetoccurs=cur.fetchone()
                    idf=float(numoftweet)/float(numoftweetoccurs)
                    tfidf[word]=tf*idf*decay[word]
                    Pti=float(wordInTweet[word])/float(numOfWord)
                    Psi=float(wordInStream[word])/float(SumOfLenthOfStream)
                    theta=lemda*Pti+(1-lemda)*Psi
                    
                sumoftfidf=sum(tfidf)
                for summary in summaries[number]:
                    sameword=[word for word in stemwords_tweet if word in summary]
                    for word in sameword:
                        Pti=float(wordInTweet[word])/float(numOfWord)
                        Psi=float(wordInStream[word])/float(SumOfLenthOfStream)
                        theta=lemda*Pti+(1-lemda)*Psi
                        
                cur.execute('insert into tweet_query, values((%s),(%s),(%s),(%s)',(str(tweet['id']), number, sumoftfidf, kld)
                conn.commit()
                
      
      
if __name__=='__main__':
    conn = pymysql.connect(host='localhost', port=3306,user='root',passwd='password',charset='UTF8mb4')
    cur = conn.cursor()
    cur.execute('create database if not exists mysql')
    conn.commit()
    conn.select_db('mysql')
    conn.commit()
    #cur.execute('drop table if exists words')
    #conn.commit()
    #cur.execute('create table if not exists words (word varchar(255) not null primary key, lastTime bigint, tf bigint)')
    #conn.commit()
    cur.execute('drop table if exists queries')
    conn.commit()
    cur.execute('create table if not exists queries (query varchar(255) not null primary key, numOfTweet bigint, numOfWord bigint)')
    conn.commit()
    cur.execute('drop table if exists word_query')
    conn.commit()
    cur.execute('create table if not exists word_query (word varchar(255), query varchar(255), tf bigint, numOfTweetOccurs bigint), primary key (word, query)')
    conn.commit()
    cur.execute('drop table if exists tweet_query')
    conn.commit()
    cur.execute('create table if not exists tweet_query (tweet varchar(255), query varchar(255), tfidf float, kld float,tweetcontent varchar(255)),primary key (tweet, query)')
    conn.commit()
    summaries={}
    wordInStream={}
    word_timestamp={}
    word_decay={}
    SumOfLenthOfStream=0
    lemda=0.9
    #SumOfLenthOfTweet=0
    consumer_key="LVKmQgPwlxnDYkEgIUYyvJ1q3"
    consumer_secret="EDzft1TESd8huGgKJt5pvj1TzDOdHqsbdf1zF8MAcd1hrqQbI6"
    
    access_token="2910563640-7Aer9hentGM4P43b8CZF8dDnwqH9V3Q2XETJSAr"
    access_token_secret="iYBCfLs3TUT7Yl54ftJoYLuM81Mupy2SbshRBs4N9ffLA"
    
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    #api = tweepy.API(auth, proxy='23.83.235.65:NDljMmVhNT@127.0.0.1:1080')
    api = tweepy.API(auth)
    #api = tweepy.API(auth,proxy="") 
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    #myStream.filter(track=['python'])
    myStream.sample()
