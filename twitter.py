import tweepy
import os
import urllib.request
import json
from board import Board, Piece

class StreamListener(tweepy.StreamListener):
    
    def send_covid_tweet(self, data, msg):
        # gets covid data
        with urllib.request.urlopen('https://api.covidtracking.com/v1/us/daily.json') as request:
            covid_data = json.loads(request.read().decode())

            days_ago = 0
            if len(msg) > 2:
                days_ago = int(msg[2])

            stats = covid_data[days_ago]
            raw_date = str(stats['date'])
            date = raw_date[:4] + '-' + raw_date[4:6] + '-' + raw_date[6:]

            # sends the status
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

    # gets status events from twitter
    def on_status(self, status):
        data = status._json
        
        msg = data['text'].split(' ')

        if len(msg) > 1 and msg[1] == 'covid':
            self.send_covid_tweet(data, msg)

        print(msg)
        if len(msg) == 3 and msg[1] == 'tictactoe':
            try:
                win = board.turn(Piece.CROSS, int(msg[2]) - 1)
                print(win)
            except:
                print('error')

            # sends messages
            if win == '-1':
                api.update_status(board.board_string() + '\nStalemate')
            elif win:
                api.update_status(board.board_string() + '\nWinner: ' + win.value)
            else:
                api.update_status(board.board_string())

#authentication information
auth = tweepy.OAuthHandler(consumer_key=os.getenv('CONSUMER_KEY'),
                           consumer_secret=os.getenv('CONSUMER_SECRET'))
auth.set_access_token(os.getenv('API_KEY'), 
                      os.getenv('API_SECRET'))

api = tweepy.API(auth)

# initialize the board
board = Board()
api.update_status(board.board_string())

# stream listener
streamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=streamListener)

stream.filter(track=['@' + api.me().screen_name])