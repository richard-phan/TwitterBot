import tweepy
import os
import urllib.request
import json

class StreamListener(tweepy.StreamListener):
    
    def send_tweet(self, data, msg):
        with urllib.request.urlopen('https://api.covidtracking.com/v1/us/daily.json') as request:
            covid_data = json.loads(request.read().decode())

            days_ago = 0
            if len(msg) > 1:
                days_ago = int(msg[1])

            stats = covid_data[days_ago]
            raw_date = str(stats['date'])
            date = raw_date[:4] + '-' + raw_date[4:6] + '-' + raw_date[6:]

            api.update_status(
                'COVID STATISTICS'
                + '\n--------------------'
                + '\nDate: ' + date 
                + '\nConfirmed cases: ' + str(stats['positive'])
                + '\nNew cases: ' + str(stats['positiveIncrease'])
                + '\nDeaths: ' + str(stats['death'])
                + '\nNew deaths: ' + str(stats['deathIncrease'])
                + '\nCurrently hospitalized: ' + str(stats['hospitalizedCurrently'])
                + '\nTotal hospitalized: ' + str(stats['hospitalized']),
                in_reply_to_status_id=data['id']
            )

    def on_status(self, status):
        data = status._json
        
        msg = data['text'].split(' ')

        self.send_tweet(data, msg)

auth = tweepy.OAuthHandler(consumer_key=os.getenv('CONSUMER_KEY'),
                           consumer_secret=os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('API_KEY'), 
                      os.getenv('API_SECRET'))

api = tweepy.API(auth)

streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)

stream.filter(track=['@' + api.me().screen_name])