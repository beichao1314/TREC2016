# from datetime import datetime
import datetime
import time as T
from email.utils import parsedate


class Time(object):
    def __init__(self, firsttime):
        self.firsttime = parsedate(firsttime)
        self.firsttime = datetime.datetime.fromtimestamp(T.mktime(self.firsttime))

    def calculatetime(self, time):
        time = parsedate(time)
        time = datetime.datetime.fromtimestamp(T.mktime(time))
        t = (time - self.firsttime).days
        return t

    def settime(self):
        self.firsttime = self.firsttime + datetime.timedelta(hours=24)
