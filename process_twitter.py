# -*- coding: utf-8 -*-
"""
Created on Mon May  9 12:14:57 2016

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
            
filepath1='F:/twitter/07/'
#corpus_words={}
list1=os.listdir(filepath1)
filepath_interest_profile='E:/TREC/interest_profile.xml'
tree = ET.parse(filepath_interest_profile)
#print(tree)
rootr = tree.getroot()
#print(rootr)
for tweets in rootr:
    corpus=[]
    corpus_id=[]
    corpus_interest_profile=[]
    corpus_words_time={}
    corpus_text=[]
    stream_word=[]
    numOfTwitter=0
    i=0
    length=0
    decay={}
    tfidf=[]
    summary=[]
    summary_tfidf=[]
    summary_KLd=[]
    number=tweets.find('Number').text
    #print(number)
    title=tweets.find('title').text
    #print(title)
    titlewords=nltk.word_tokenize(title)
    titlewords=filters(titlewords)
    removeStopWords_interest_profile=removeStopWords_1(titlewords)
    #print(removeStopWords)
    stemwords_interest_profile=StemWords(removeStopWords_interest_profile)
    for files1 in list1:
        filepath2=os.path.join(filepath1,files1)
        list2=os.listdir(filepath2)
        numOfTwitterOfDay=0
        with open('E:/TREC/summary/summary.txt','a')as fa:
            fa.write('day: '+files1+'\n')
            fa.write('________________________________________'+'\n')
            
        for files2 in list2:
            filepath3=os.path.join(filepath2,files2)
            list3=os.listdir(filepath3)
            for files3 in list3:
                filepath4=os.path.join(filepath3,files3)
                with bz2file.open(filepath4,'r') as f:
                    print(filepath4+'; time: '+time.strftime('%X',time.localtime(time.time())))
                    number=tweets.find('Number').text
                    #print(number)
                    title=tweets.find('title').text
                    #print(title)
                    titlewords=nltk.word_tokenize(title)
                    titlewords=filters(titlewords)
                    removeStopWords_interest_profile=removeStopWords_1(titlewords)
                    #print(removeStopWords)
                    stemwords_interest_profile=StemWords(removeStopWords_interest_profile)
                    n=0
                    for line in f: 
                        #line=str(line)
                        line=str(line, encoding = "utf-8")
                        if line[:10]=='{"delete":':
                            continue
                        #print(line)
                        tweet=json.loads(line)
                        #print(tweet['id'])
                        #print(type(tweet['lang']))
                        #print(tweet['text'])
                        #print(tweet['created_at'])
                        #print(tweet['favorite_count'])
                        #print(tweet['retweet_count'])
                        #print(tweet['user'])
                        #print(tweet['entities'])
                        if tweet['lang']=='en':
                            #print(type(tweet['id']))
                            #print(tweet['lang'])
                            if 'retweeted_status' in tweet:
                                content=tweet['retweeted_status']['text']
                                #print(tweet['id'])
                            else:
                                content=tweet['text']
                        else:
                            continue
                        
                        #print(content)
                        #print('***********')
                        results=re.compile(r'http://[a-zA-Z0-9.?/&=:]*',re.S)
                        content=results.sub("",content)
                        #print(content)
                        #print('___________________')
                        words=nltk.word_tokenize(content)
                        word=filters(words)
                        removeStopWords=removeStopWords_1(word)
                        stemwords=StemWords(removeStopWords)
                        #print(type(stemwords))
                        #corpus_words[n+i]=stemwords
                        text=' '.join(stemwords)
                        count=0
                        stream_word.append(text)
                        for wordsss in removeStopWords_interest_profile:
                            if wordsss in stemwords:
                                count+=1
                        if count>=2:    
                            words_decay={}
                            for word in stemwords:
                                if not(word in corpus_words_time):
                                    corpus_words_time[word]=float(tweet['timestamp_ms'])
                                    words_decay[word]=1
                                    continue
                                else:
                                    deta=float(tweet['timestamp_ms'])-corpus_words_time[word]
                                    if deta < 7200000:
                                        sss=((float(deta-3600000.0))/3600000.0)*((float(deta-3600000.0))/3600000.0)
                                        words_decay[word]=sss
                                    else:
                                        words_decay[word]=1
                            decay[i+n]=words_decay
                            
                            #print(text)
                            corpus.append(text)
                            corpus_id.append(tweet['id_str'])
                            corpus_interest_profile.append(number)
                            #corpus_text.append(content)
                            #print(stemwords)
                            #print('______________________________________________')
                            #print(n)
                            n+=1
                newlength=len(corpus)
                if newlength-length>0:
                    length=newlength
                    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
                    #print vectorizer          
                    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
                    #print transformer            
                    tfidfs=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵  
                    #print type(tfidf)            
                    corpus_word=vectorizer.get_feature_names()#获取词袋模型中的所有词语  
                    #print word
                    weight=tfidfs.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
                    print('______________________')
                    while(i<len(corpus)):                      
                        #for id_str in corpus_id[i:]:
                        d={}
                        for j in range(len(corpus_word)):
                            d[corpus_word[j]]=weight[i][j]
                        tfidf_i=0
                        #print(len(decay))
                        for word in corpus_word:
                            #print(word)
                            #print(decay[i])
                            if not(word in decay[i]):
                                continue
                            else:
                                tfidf_i+=decay[i][word]*d[word]
                        #strs='inerest profile:'+ corpus_interest_profile[i]+' '+'id_str:'+corpus_id[i] +' '+'tfidf:'+ str(tfidf)+'\n'
                        #print(strs)
                        tfidf.append(tfidf_i)
                        """with open('E:/TREC/tfidf/tfidf.txt','a') as fa:
                            fa.write(strs)"""
                            #print(time.strftime('%X',time.localtime(time.time())))
                            #print('print completed! i='+str(i)+'; time: '+time.strftime('%X',time.localtime(time.time())))
                        if len(summary)==0:
                                with open('E:/TREC/summary/summary.txt','a')as fa:
                                    fa.write(corpus_interest_profile[i]+': '+'id_str: '+corpus_id[i]+'\n'+'text: '+'\n'+corpus[i]+'\n')
                                    fa.write('\n')
                                    print('publish a twitter!'+' time: '+time.strftime('%X',time.localtime(time.time())))
                        else:
                            if tfidf[i]>=max(summary_tfidf):
                                #KLd=KLdivergence(corpus[i],summary,stream_word(0:(stream_word.index(corpus[i])+1)),i)
                                KLd=0.0
                                KLD=[]
                                for summ in summary:
                                    kld=0.0
                                    summ_word=nltk.word_tokenize(summ)
                                    sameWords=[word for word in summ_word if word in nltk.word_tokenize(corpus[i])]
                                    Ti=calTheta(sameWords, stream_word[0:stream_word.index(corpus[i])+1])                                    
                                    Tj=calTheta(sameWords, stream_word[0:stream_word.index(summ)+1])
                                    for word in sameWords:
                                        kld+=(Ti[word]*math.log(Ti[word]/Tj[word]))
                                    KLD.append(kld)
                                KLd=min(KLD)
                                if KLd>=max(summary_KLd) and numOfTwitterOfDay<10:
                                    summary.append(corpus[i])
                                    summary_tfidf.append(tfidf(i))
                                    summary_KLd.append(KLd)
                                    numOfTwitterOfDay+=1
                                    with open('E:/TREC/summary/summary.txt','a')as fa:
                                        fa.write(corpus_interest_profile[i]+': '+'id_str: '+corpus_id[i]+'\n'+'text: '+'\n'+corpus[i]+'\n')
                                        fa.write('\n')
                                        print('publish a twitter!'+' time: '+time.strftime('%X',time.localtime(time.time())))
                                        
                        i+=1