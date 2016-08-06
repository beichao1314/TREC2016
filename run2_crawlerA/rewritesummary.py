import pymysql
from process import preprocess
import time as T
import nltk
import math
import operator


class PushSummary():
    def __init__(self, lemda, interest_files, time, rest, fa, topicid):
        self.topicid = topicid
        self.L = len(self.topicid)
        self.SumOfLenthOfStream = 0
        self.wordInStream = {}
        self.lemda = lemda
        self.interest_files = interest_files
        self.time = time
        self.day = 1
        self.rest = rest
        self.fa = fa
        self.tfidfthresholdA = []
        self.jsdthresholdA = []
        self.lmsthresholdA = []
        self.tfidfthresholdB = []
        self.jsdthresholdB = []
        self.lmsthresholdB = []
        self.numofdayA = []
        self.numofdayB = []
        self.queries_numOfTweet = []
        self.queries_numOfWord = []
        self.queries_word = []
        self.queries_occur = []
        self.summaryA = []
        self.summaryB = []
        self.qoccur = []
        self.numofq = []
        self.numofqinstream = {}
        for i in range(self.L):
            # self.numofdayA[number] = 0
            # self.numofdayB[number] = 0
            self.numofdayA.append(0)
            self.numofdayB.append(0)

            self.queries_word.append({})
            self.queries_occur.append({})
            self.summaryA.append([])
            self.summaryB.append([])
            # self.word_tweet_query.append({})
            self.qoccur.append({})
            self.numofq.append({})
            self.tfidfthresholdA.append(0.7)
            self.jsdthresholdA.append(0.04)
            self.lmsthresholdA.append(0.02)
            self.tfidfthresholdB.append(0.5)
            self.jsdthresholdB.append(0.04)
            self.lmsthresholdB.append(0.02)
            self.queries_numOfTweet.append(0)
            self.queries_numOfWord.append(0)

    def pushSummarys(self, tweet):
        if ('delete' not in tweet) and (tweet['lang'] == 'en'):
            if 'retweeted_status' in tweet:
                tem = tweet['retweeted_status']
                tem['timestamp_ms'] = tweet['timestamp_ms']
                tem['created_at'] = tweet['created_at']
                tweet = tem
            delta = self.time.calculatetime(tweet['created_at'])
            if delta == 1:
                for x in range(self.L):
                    stemwords_interest_profile = self.interest_files[x]
                    self.numofdayA[x] = 0
                    self.numofdayB[x] = 0
                    listofsummaryA = [summary[0] for summary in self.summaryA[x] if summary[1] == self.day]
                    if len(listofsummaryA) > 0:
                        self.tfidfthresholdA[x] = min(summaryA[2] for summaryA in listofsummaryA)

                    listofsummaryB = [summary[0] for summary in self.summaryB[x] if summary[1] == self.day]
                    if len(listofsummaryB) > 0:
                        self.tfidfthresholdB[x] = min(summaryB[2] for summaryB in listofsummaryB)
                        sumoflen = sum(summaryBBBB[5] for summaryBBBB in listofsummaryB)
                        ADL = sumoflen / len(listofsummaryB)
                        lenofq = len(stemwords_interest_profile)
                        result = []
                        for summaryBBB in listofsummaryB:
                            score = 0
                            TF = summaryBBB[4]
                            for q in stemwords_interest_profile:
                                tf = TF[q]
                                avgtf = sum(TF[qq] for qq in stemwords_interest_profile) / len(TF)
                                RITF = math.log2(1 + tf) / math.log2(1 + avgtf)
                                LRTF = tf * math.log2(1 + ADL / summaryBBB[5])+0.0001
                                w = 2 / (1 + math.log2(1 + lenofq))
                                TFF = w * RITF / (1 + RITF) + (1 - w) * LRTF / (1 + LRTF)
                                IDF = math.log((len(listofsummaryB) + 1) / (self.qoccur[x][q] + 1)) + 0.0001
                                AEF = self.numofq[x][q] / (self.qoccur[x][q] + 1)
                                TDF = IDF * AEF / (1 + AEF)
                                sim = TFF * TDF
                                score += sim
                                del tf, avgtf, RITF, LRTF, w, TFF, IDF, AEF, TDF, sim
                            result.append([score, summaryBBB[1]])
                        del listofsummaryB
                        result.sort(key=operator.itemgetter(0), reverse=True)
                        j = 1
                        for i in result:
                            if (self.day) > 9:
                                d = '201608' + str(self.day)
                            else:
                                d = '2016080' + str(self.day)
                            with open('B.txt', 'a') as ff:
                                ff.write(
                                    '%s %s Q0 %s %s %s CCNUNLPrun2\n' % (
                                        d, self.topicid[x], i[1], str(j), i[0]))
                            j = j + 1
                self.time.settime()
                self.day = self.day + 1
            content = tweet['text']
            stemwords_tweet = preprocess(content)
            del content
            wordInTweet = {}
            if stemwords_tweet == False:
                pass
            else:
                numOfWordAtweet = len(stemwords_tweet)
                self.SumOfLenthOfStream = numOfWordAtweet + self.SumOfLenthOfStream
                id_str = tweet['id_str']
                for word in stemwords_tweet:
                    if word in self.wordInStream:
                        self.wordInStream[word] += 1
                    else:
                        self.wordInStream[word] = 1
                    if word in wordInTweet:
                        wordInTweet[word] += 1
                    else:
                        wordInTweet[word] = 1
                for x in range(self.L):
                    stemwords_interest_profile = self.interest_files[x]
                    for q in stemwords_interest_profile:
                        if q in self.numofqinstream:
                            self.numofqinstream[q] += stemwords_tweet.count(q)
                        else:
                            self.numofqinstream[q] = stemwords_tweet.count(q)
                for x in range(self.L):
                    stemwords_interest_profile = self.interest_files[x]
                    count = sum(stemwords_tweet.count(wordsss) for wordsss in stemwords_interest_profile)
                    lenofq = len(stemwords_interest_profile)
                    if count >= 1:
                        qt = {}
                        for qqq in stemwords_interest_profile:
                            if qqq in qt:
                                qt[qqq] += stemwords_tweet.count(qqq)
                            else:
                                qt[qqq] = stemwords_tweet.count(qqq)
                        lms = 0
                        samewords = [q for q in stemwords_interest_profile if q in stemwords_tweet]
                        for qq in samewords:
                            Pq = self.lemda * 1.0 / float(lenofq) + (1 - self.lemda) * float(
                                self.numofqinstream[qq]) / float(
                                self.SumOfLenthOfStream)
                            Pt = self.lemda * qt[qq] / float(numOfWordAtweet) + (1 - self.lemda) * float(
                                self.numofqinstream[qq]) / float(self.SumOfLenthOfStream)
                            M = 0.5 * (Pq + Pt)
                            lms += 0.5 * Pq * math.log(Pq / M) + 0.5 * Pt * math.log(Pt / M)
                        if lms <= self.lmsthresholdA[x]:
                            sumoftfidf = 0.0
                            for word in stemwords_tweet:
                                if word in self.queries_word[x]:
                                    self.queries_word[x][word] += 1
                                else:
                                    self.queries_word[x][word] = 1
                            for word in set(stemwords_tweet):
                                if word not in self.queries_occur[x]:
                                    self.queries_occur[x][word] = 1
                                else:
                                    self.queries_occur[x][word] += 1

                            self.queries_numOfWord[x] += numOfWordAtweet
                            self.queries_numOfTweet[x] += 1

                            for word in stemwords_tweet:
                                tf = self.queries_word[x][word] / self.queries_numOfWord[x]
                                idf = math.log2((self.queries_numOfTweet[x] + 1) / self.queries_occur[x][word])
                                sumoftfidf = sumoftfidf + tf * idf
                            if sumoftfidf >= self.tfidfthresholdA[x] and self.numofdayA[x] < 10:
                                listofsummaryA = [summary[0] for summary in self.summaryA[x]]
                                if len(listofsummaryA) > 0:
                                    jsd = []
                                    for summary in listofsummaryA:
                                        sumofjsd = 0
                                        tf = {}
                                        for wordss in summary[0]:
                                            if wordss in tf:
                                                tf[wordss] += 1
                                            else:
                                                tf[wordss] = 1
                                        sameword = [word for word in stemwords_tweet if
                                                    word in summary[0]]
                                        if len(sameword) > 0:
                                            for word in sameword:
                                                Pti = float(wordInTweet[word]) / float(numOfWordAtweet)
                                                Psi = float(self.wordInStream[word]) / float(self.SumOfLenthOfStream)
                                                thetaTi = self.lemda * Pti + (1 - self.lemda) * Psi
                                                Ptj = float(tf[word]) / float(len(summary[0]))
                                                Psj = float(self.wordInStream[word]) / float(self.SumOfLenthOfStream)
                                                thetaTj = self.lemda * Ptj + (1 - self.lemda) * Psj
                                                # sumofjsd += thetaTi * math.log(thetaTi / thetaTj)
                                                M = float((thetaTi + thetaTj) / 2)
                                                sumofjsd += 0.5 * (thetaTi * math.log(thetaTi / M)) + 0.5 * (
                                                    thetaTj * math.log(thetaTj / M))
                                            jsd.append(sumofjsd)
                                        else:
                                            jsd.append(0.06)
                                    JSD = min(jsd)
                                else:
                                    JSD = 0.04
                                # print('kld:' + str(JSD))
                                if JSD >= self.jsdthresholdA[x]:
                                    #self.rest.Post(self.topicid[x], id_str)
                                    self.lmsthresholdA[x] = lms
                                    self.jsdthresholdA[x] = JSD
                                    self.numofdayA[x] += 1
                                    a = [stemwords_tweet, id_str, sumoftfidf, JSD]
                                    self.summaryA[x].append([a, self.day])
                                    self.fa.write('%s %s tfidf:%s jsd:%s lms:%s\n' % (self.day, self.topicid[x], sumoftfidf, JSD,lms))
                        if lms <= self.lmsthresholdB[x]:
                            sumoftfidf = 0.0
                            for word in stemwords_tweet:
                                if word in self.queries_word[x]:
                                    self.queries_word[x][word] += 1
                                else:
                                    self.queries_word[x][word] = 1
                            for word in set(stemwords_tweet):
                                if word not in self.queries_occur[x]:
                                    self.queries_occur[x][word] = 1
                                else:
                                    self.queries_occur[x][word] += 1

                            self.queries_numOfWord[x] += numOfWordAtweet
                            self.queries_numOfTweet[x] += 1

                            for word in stemwords_tweet:
                                tf = self.queries_word[x][word] / self.queries_numOfWord[x]
                                idf = math.log2((self.queries_numOfTweet[x] + 1) / self.queries_occur[x][word])
                                sumoftfidf = sumoftfidf + tf * idf
                            if sumoftfidf >= self.tfidfthresholdB[x] and self.numofdayB[x] < 100:
                                listofsummaryB = [summary[0] for summary in self.summaryB[x]]
                                if len(listofsummaryB) > 0:
                                    jsd = []
                                    for summary in listofsummaryB:
                                        sumofjsd = 0
                                        sameword = [word for word in stemwords_tweet if word in summary[0]]
                                        tf = {}
                                        for wordss in summary[0]:
                                            if wordss in tf:
                                                tf[wordss] += 1
                                            else:
                                                tf[wordss] = 1
                                        if len(sameword) > 0:
                                            for word in sameword:
                                                Pti = float(wordInTweet[word]) / float(numOfWordAtweet)
                                                Psi = float(self.wordInStream[word]) / float(self.SumOfLenthOfStream)
                                                thetaTi = self.lemda * Pti + (1 - self.lemda) * Psi
                                                Ptj = float(tf[word]) / float(len(summary[0]))
                                                Psj = float(self.wordInStream[word]) / float(self.SumOfLenthOfStream)
                                                thetaTj = self.lemda * Ptj + (1 - self.lemda) * Psj
                                                # sumofjsd += thetaTi * math.log(thetaTi / thetaTj)
                                                M = float((thetaTi + thetaTj) / 2)
                                                sumofjsd += 0.5 * (thetaTi * math.log(thetaTi / M)) + 0.5 * (
                                                    thetaTj * math.log(thetaTj / M))
                                            jsd.append(sumofjsd)
                                        else:
                                            jsd.append(0.06)
                                    JSD = min(jsd)
                                else:
                                    JSD = 0.04
                                if JSD >= self.jsdthresholdB[x]:
                                    self.numofdayB[x] += 1
                                    lenoflistB=len(listofsummaryB)
                                    self.jsdthresholdB[x]=(self.jsdthresholdB[x]*lenoflistB+JSD)/(lenoflistB+1)
                                    self.lmsthresholdB[x]=(self.lmsthresholdB[x]*lenoflistB+JSD)/(lenoflistB+1)
                                    TF = {}
                                    for q in stemwords_interest_profile:
                                        TF[q] = stemwords_tweet.count(q)
                                        if q in stemwords_tweet:
                                            if q in self.qoccur[x]:
                                                self.qoccur[x][q] += 1
                                            else:
                                                self.qoccur[x][q] = 1
                                        else:
                                            self.qoccur[x][q] = 0
                                        if q in self.numofq[x]:
                                            self.numofq[x][q] += stemwords_tweet.count(q)
                                        else:
                                            self.numofq[x][q] = stemwords_tweet.count(q)
                                    b = [stemwords_tweet, id_str, sumoftfidf, JSD, TF, numOfWordAtweet]
                                    self.summaryB[x].append([b, self.day])
        pass
