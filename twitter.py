# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:20:06 2016

@author: xiaobei
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = " 2910563640-7Aer9hentGM4P43b8CZF8dDnwqH9V3Q2XETJSAr"
access_token_secret = " iYBCfLs3TUT7Yl54ftJoYLuM81Mupy2SbshRBs4N9ffLA"
consumer_key = " LVKmQgPwlxnDYkEgIUYyvJ1q3"
consumer_secret = " EDzft1TESd8huGgKJt5pvj1TzDOdHqsbdf1zF8MAcd1hrqQbI6"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])