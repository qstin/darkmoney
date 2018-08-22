import tweepy, sys
import gspread


def authorizeTwitter():
    CONSUMER_KEY = '9h6dAiEPc4QcjiqYeApN0Ogzm'
    CONSUMER_SECRET = 'aIdsH1lJeFJvwpZ5F6zn5kWfitHIjE7m9cUJoqpWHbkyYxNXpX'
    ACCESS_KEY = '4854183897-2d3LxGt6Nia3dBP5LPb8FsrZ3Pw8iTePiMciUv0'
    ACCESS_SECRET = 'SSdbFdGB84soQRvjIAmrgj0XOP8CUNgQzwuOZoupboj9L'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

    return api

def sendTweet(api, tweet):

    api.update_status(tweet)



