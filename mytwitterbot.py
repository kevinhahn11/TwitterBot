
import tweepy
import tkinter
from tkinter import *
consumer_key = "" #api key
consumer_secret = "" #api secret
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Sanity Checking:
user = api.me()
print(user.name) # should print my twitter account name
""" Follow every user that follows you
for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    print("Followed everyone that is following " + user.name)
    # follows all the people following me
"""
# To retweet tweets about a particular topic
###################################
# To favorite tweets about a topic:
"""
search = "Netflix"
numOfTweets = 2
for tweet in tweepy.Cursor(api.search, search).items(numOfTweets):
    try: 
        tweet.favorite()
        print('Favorited the tweet')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
"""
"""
# Reply to a user based on a keyword:
tweetID = "Andy McCullough" # their screen name (bold letters)
username = "McCulloughTimes" # their handle @personsUsername

replyPhrase = "Nice"
for tweet in tweepy.Cursor(api.search, search).items(numOfTweets):
    try: 
        tweetID = "Andy McCullough"
        username = "McCulloughTimes"
        api.update_status("@" + username + " " + replyPhrase, in_reply_to_status_id = tweetID)
        print("Replied with " + replyPhrase)
    
    except tweepy.TweepError as e:
        print(e.reason)
"""        
####################################
# Creating the GUI:
root = Tk()
label1 = Label( root, text="Search")
E1 = Entry(root, bd =5)

label2 = Label( root, text="Number of Tweets")
E2 = Entry(root, bd =5)

label3 = Label( root, text="Response")
E3 = Entry(root, bd =5)

label4 = Label( root, text="Reply?")
E4 = Entry(root, bd =5)

label5 = Label( root, text="Retweet?")
E5 = Entry(root, bd =5)

label6 = Label( root, text="Favorite?")
E6 = Entry(root, bd =5)

label7 = Label( root, text="Follow?")
E7 = Entry(root, bd =5)

####################################
def getE1():
    return E1.get()
def getE2():
    return E2.get()
def getE3():
    return E3.get()
def getE4():
    return E4.get()
def getE5():
    return E5.get()
def getE6():
    return E6.get()
def getE7():
    return E7.get()

def mainFunction():
    getE1()
    search = getE1()
    
    getE2()
    numberOfTweets = getE2()
    numberOfTweets = int(numberOfTweets)
    
    getE3()
    phrase = getE3()
    
    getE4()
    reply = getE4()
    
    getE5()
    retweet = getE5()
    
    getE6()
    favorite = getE6()
    
    getE7()
    follow = getE7()
    
    
    if reply == "yes":
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                tweetID = tweet.user.id
                username = tweet.user.screen_name
                api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetID)
                print("Replied with " + phrase)
                
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
    if retweet == "yes":
        #search = "Friedman"
        numOfTweets = 1
        for tweet in tweepy.Cursor(api.search, search).items(numOfTweets):
            try: 
                tweet.retweet()
                print('Retweeted the tweet')
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
    if favorite == "yes":
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                tweet.favorite()
                print('Favorited the tweet')
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break;
    if follow == "yes":
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                tweet.user.follow()
                print('Followed the user')
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
        
    
submit = Button(root, text = "Submit", command = mainFunction)
        
label1.pack()
E1.pack()
label2.pack()
E2.pack()
label3.pack()
E3.pack()
label4.pack()
E4.pack()
label5.pack()
E5.pack()
label6.pack()
E6.pack()
label7.pack()
E7.pack()
submit.pack(side=BOTTOM)
root.mainloop()
"""
import re # for preprocessing
import pickle
import tweepy
from tweepy import OAuthHandler

# Initialize the keys
consumer_key = ''
consumer_secret = '' 
access_token = ''
access_token_secret = '' 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
args = ['google'] # tweets containing this word
api = tweepy.API(auth, timeout=10)
# after 10 seconds, it will stop looking
# for tweets that contain 'facebook'

# fetching real time tweets
listOfTweets = []
query = args[0] # what we are looking for i.e. tweets with 'facebook' in them
if len(args) == 1:
    for status in tweepy.Cursor(api.search, q=query+" -filter:retweets", lang='en', result_type='recent').items(100):
        listOfTweets.append(status.text)

totalPositives = 0
totalNegs = 0

with open('tfidfmodel.pickle', 'rb') as f:
    vectorizer = pickle.load(f)
with open('classifier.pickle', 'rb') as f:
    clf = pickle.load(f)
    
# preprocess the tweets
# Preprocessing the tweets
for tweet in listOfTweets:
    tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " ", tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$", " ", tweet)
    tweet = tweet.lower()
    tweet = re.sub(r"that's","that is",tweet)
    tweet = re.sub(r"there's","there is",tweet)
    tweet = re.sub(r"what's","what is",tweet)
    tweet = re.sub(r"where's","where is",tweet)
    tweet = re.sub(r"it's","it is",tweet)
    tweet = re.sub(r"who's","who is",tweet)
    tweet = re.sub(r"i'm","i am",tweet)
    tweet = re.sub(r"she's","she is",tweet)
    tweet = re.sub(r"he's","he is",tweet)
    tweet = re.sub(r"they're","they are",tweet)
    tweet = re.sub(r"who're","who are",tweet)
    tweet = re.sub(r"ain't","am not",tweet)
    tweet = re.sub(r"wouldn't","would not",tweet)
    tweet = re.sub(r"shouldn't","should not",tweet)
    tweet = re.sub(r"can't","can not",tweet)
    tweet = re.sub(r"couldn't","could not",tweet)
    tweet = re.sub(r"won't","will not",tweet)
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet = re.sub(r"\s+[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+[a-z]$"," ",tweet)
    tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+"," ",tweet)
    # print(tweet)
    sentiment = clf.predict(vectorizer.transform([tweet]).toarray())
    # print(tweet, ":", sentiment)
    if sentiment[0] == 1:
        totalPositives += 1
    else:
        totalNegs += 1

import matplotlib.pyplot as plt
import numpy as np
objects = ['Positive', 'Negative']
y_pos = np.arange(len(objects))

plt.bar(y_pos, [totalPositives, totalNegs],alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number')
plt.title('Amount of Positive and Negative Tweets')

plt.show()
"""
