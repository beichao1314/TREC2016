# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:20:08 2016

@author: xiaobei
"""

import xml.etree.ElementTree as ET 
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn  
import gensim
import xml.dom.minidom

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
    
if __name__=='__main__':
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'top', None)
    root = dom.documentElement
    model = gensim.models.Word2Vec.load_word2vec_format("E:/socialtimeline/wikipedia/wiki/wiki.en.text.vector", binary=False)
    filepath='E:/TREC/interest_profile.xml'
    tree = ET.parse(filepath)
    #print(tree)
    rootr = tree.getroot()
    #print(rootr)
    for i in rootr:
        
        number=i.find('Number').text
        #print(number)
        title=i.find('title').text
        #print(title)
        #desc=i.find('Description').text
        #print(desc)
        #narr=i.find('Narrative').text
        #print(narr)
        #words=nltk.word_tokenize(narr)
        words=nltk.word_tokenize(title)
        #print(words)
        word=filters(words)
        #print(words)
        #removeStopWords=removeStopWords_1(word)
        #print(removeStopWords)
        stemwords=StemWords(word)
        #print(stemwords)
        #tags=nltk.pos_tag(stemwords)
        #print(tags)
        """NandV=[]
        for word in tags:
            if word[1]=='NN':
               NandV.append(word[0]) """
        #print(NandV)
        similar={}
        for word in stemwords:
            """if not(word in model.vocabulary):
                print(word)
                continue"""
            similarword=model.most_similar(word)
            similar[word]=similarword
        print(number)
        #print(type(similarword))
        #for word in NandV:
            #print(similar[word][0:])
        employee = dom.createElement('item')
        root.appendChild(employee)
        nameE=dom.createElement('Num')
        nameT=dom.createTextNode(number)
        nameE.appendChild(nameT)
        employee.appendChild(nameE)
        ageE=dom.createElement('extension')
        ageT=dom.createTextNode(str(similar))
        ageE.appendChild(ageT)
        employee.appendChild(ageE)
    with open('E:/TREC/interest_profile_extension(title).xml','w',encoding='utf-8') as f:
        dom.writexml(f, addindent='  ', newl='\n',encoding='utf-8')