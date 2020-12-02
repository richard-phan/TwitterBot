import tweepy

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print(status.text)


auth = tweepy.OAuthHandler(consumer_key='Thkg7wftUYpTaDzHWOQFHN8Pj',
                           consumer_secret='zr8hkYXvTBcmI3NmCU3lIdvlJfqliKpXbaxKitjD7fg0PMhJWf')
auth.set_access_token('1224788279381262336-BgbFJjrqktqhiowCrBRKcfyMPQJ4zH', 
                      'YHtojSlaQM8LnzxrKVLwqzeEaUJ4iyPGhqqWjF9VXORwX')

api = tweepy.API(auth)

streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)

stream.filter(track=['@Richard48887283'])