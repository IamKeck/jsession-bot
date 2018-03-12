#!/usr/bin/env python
from os import environ
import tweepy
import datetime

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(environ["CK"], environ["CS"])
auth.set_access_token(environ["AT"], environ["AS"])

api = tweepy.API(auth)

class Listener(tweepy.StreamListener):
    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)

        if str(status.in_reply_to_screen_name)== "jsession_bot":
            tweet = "@" + str(status.user.screen_name) + " " + "Hello！\n" + str(datetime.datetime.today())
            api.update_status(status=tweet, in_reply_to_status_id=status.id)
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True


listener = Listener()
stream = tweepy.Stream(auth, listener)
stream.filter(track=["@jsession_bot"])
