# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:19:01 2016

@author: xiaobei
"""

import xml.dom.minidom

if __name__=='__main__':
    #GenerateXml()
    impl = xml.dom.minidom.getDOMImplementation()
    dom = impl.createDocument(None, 'top', None)
    root = dom.documentElement
    filepath='E:/TREC/realtime/2015/2015_interest_profiles.txt'
    with open(filepath,'r') as f:
        data=f.readlines()
    n=0
    A=[]
    for i in data:
        n=n+1
        if i=='<top>\n':
            top=n
        if i=='</top>\n':
            down=n
            content=data[top:down]
            for j in content:
                if j=='\n':
                    content.remove(j)
            s=''
            for k in content:
                s=s+k
            A.append(s)
    #print(a)
    for a in A:
        a=a.split('\n')
        m=0
        num=''
        titlenum=0
        descnum=0
        narrnum=0
        downnum=0
        for aa in a:
            m=m+1
            if aa[0:5]=='<num>':
                num=aa[-5:]
            if aa[0:7]=='<title>':
                titlenum=m
            if aa[0:6]=='<desc>':
                descnum=m
            if aa[0:6]=='<narr>':
                narrnum=m
            if aa[0:6]=='</top>':
                downnum=m
        print(titlenum)
        print(descnum)
        title=a[titlenum:descnum-1]
        title=' '.join(title)
        desc=a[descnum:narrnum-1]
        desc=' '.join(desc)
        narr=a[narrnum:downnum-1]
        narr=' '.join(narr)
        print(num)
        print(title)
        print(desc)
        print(narr)
        employee = dom.createElement('item')
        root.appendChild(employee)
        nameE=dom.createElement('Number')
        nameT=dom.createTextNode(num)
        nameE.appendChild(nameT)
        employee.appendChild(nameE)
        ageE=dom.createElement('title')
        ageT=dom.createTextNode(title)
        ageE.appendChild(ageT)
        employee.appendChild(ageE)
        ageE=dom.createElement('Description')
        ageT=dom.createTextNode(desc)
        ageE.appendChild(ageT)
        employee.appendChild(ageE)
        ageE=dom.createElement('Narrative')
        ageT=dom.createTextNode(narr)
        ageE.appendChild(ageT)
        employee.appendChild(ageE)
        #print(a)
    with open('E:/TREC/interest_profile.xml','w',encoding='utf-8') as f:
        dom.writexml(f, addindent='  ', newl='\n',encoding='utf-8')