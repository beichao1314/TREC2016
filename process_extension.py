# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:21:31 2016

@author: xiaobei
"""
import xml.etree.ElementTree as ET 

filepath='E:/TREC/interest_profile_extension.xml'
tree = ET.parse(filepath)
#print(tree)
root = tree.getroot()
#print(root)
for i in root:
    number=i.find('Num').text
    print(number)
    extension=i.find('extension').text
    for k,v in eval(extension).items():
        print(k,v)