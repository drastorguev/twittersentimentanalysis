import tweepy
from crds import *
from textblob import TextBlob
import time
from prettytable import PrettyTable
from datetime import datetime
import sqlite3

conn = sqlite3.connect('twitterprofiles.db')
c = conn.cursor()

targettwitterprofile = 'anytwitterusername'

c.execute('CREATE TABLE '+targettwitterprofile+' (dbtweetid int PRIMARY KEY, dbtweetdate date, dbtweettext text, polarity real)')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

x = PrettyTable()
x.field_names = ["Count", "ID", "Date", "Text", "Polarity"]
n = 1

for page in tweepy.Cursor(api.user_timeline, id=targettwitterprofile, count=200).pages(20):
    for tweet in page:
        tweetid = tweet.id
        tweetdate = datetime.strptime(str(tweet.created_at)[:10],'%Y-%m-%d').strftime('%d-%m-%Y')
        tweettext = tweet.text
        polarity = round(TextBlob(tweettext).sentiment.polarity,4)
        x.add_row([n,tweetid, tweetdate, tweettext, polarity])
        c.execute("insert into "+targettwitterprofile+" values (?,?,?,?)", (tweetid, tweetdate, tweettext, polarity))
        n+=1
    time.sleep(65)

print x

conn.commit()
c.close()
