import tweepy

from .secret import consumer_key, consumer_secret, key, secret


def get_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return tweepy.API(auth)
