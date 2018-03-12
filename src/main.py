#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import environ
import tweepy
import datetime
import json
from functools import reduce
import random

print("head")

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(environ["CK"], environ["CS"])
print("auth")
auth.set_access_token(environ["AT"], environ["AS"])
print("set access token")

api = tweepy.API(auth)
print("api")

class Listener(tweepy.StreamListener):
    def set_song_list(self, song_list):
        self._song_list = song_list

    def select_song(self):
        return random.choice(self._song_list)

    def on_status(self, status):
        status.created_at += datetime.timedelta(hours=9)

        if str(status.in_reply_to_screen_name)== "jsession_bot":
            tweet = "@{} 次は{}なんていかがでしょうか?".format(status.user.screen_name, self.select_song().upper())
            api.update_status(status=tweet, in_reply_to_status_id=status.id)
        return True
    def on_event(self, evt):
        if evt.event != "follow":
            return True
        if evt.target["screen_name"] != "jsession_bot":
            return True
        print("following {}".format(evt.source["screen_name"]))
        api.create_friendship(evt.source["screen_name"])

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True

print("before open")
with open("./songs.json", "r") as songs:
    song_data = json.load(songs)

print("before reduce")
song_list = reduce(lambda acc, d: acc + [d["name"]] * d["rate"], song_data, [])
print("got song list")

print("before start")
listener = Listener()
listener.set_song_list(song_list)
stream = tweepy.Stream(auth, listener)
stream.userstream(replies="all")

