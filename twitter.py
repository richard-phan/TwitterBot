import tweepy
import os

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print(status.text)


auth = tweepy.OAuthHandler(consumer_key=os.getenv('CONSUMER_KEY'),
                           consumer_secret=os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('API_KEY'), 
                      os.getenv('API_SECRET'))

api = tweepy.API(auth)

streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)

stream.filter(track=['@Richard48887283'])