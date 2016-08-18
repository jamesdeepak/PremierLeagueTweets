"""
Example Stream listener for twitter API.
"""
from __future__ import print_function
import tweepy
import time
import cnfg
from pymongo import MongoClient


class TweetListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        client = MongoClient()
        # Use tweetdb database
        self.db = client.tweetdb

    #def on_status(self, tweet):
        #print(tweet.text)
        # If we need to save , we can put save command to save to mongodb

    def on_data(self, data):
        """This will be called each time we receive stream data"""
        # Decode JSON
        try:
            datajson = json.loads(data)

            # We only want to store tweets in English
            if "lang" in datajson and datajson["lang"] == "en":
                # Store tweet info into the cooltweets collection.
                print("Yes")
                self.db.tweetdb.insert(datajson)
        except Exception:
            print("Error in parsing data {}".format(data))

    def on_error(self, error_msg):
        print('Error: {}'.format(error_msg))

    def on_timeout(self):
        print('Timed Out.  Might be rate-limited.  Introduce Delay in the process.  ')
        time.sleep(10)

import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
twitter_config = os.path.join(CUR_DIR, "..", "twitter.cfg")

config = cnfg.load(twitter_config)

auth = tweepy.OAuthHandler(config["consumer_key"],
                           config["consumer_secret"])
auth.set_access_token(config["access_token"],
                      config["access_token_secret"])


tweet_listener = TweetListener()
tweet_stream = tweepy.Stream(auth = auth, listener=tweet_listener)

tweet_stream.filter(track=['#lfc','@lfc','lfc', 'liverpool','klopp','BurLiv'
    , '#BurLiv', '#LivBur','LivBur'
    ,'@BurnleyOfficial','BurnleyOfficial','Burnley','#Bur'])
