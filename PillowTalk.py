#Author: Omar Ansari
#Verison 1.0

?from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
import datetime
import RPi.GPIO as GPIO


CONSUMER_KEY = 'XXXXXXXX'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXX'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = 'XXXXXXXXXXXXX'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'XXXXXXXXXXXXX'#keep the quotes, replace this with your access token secret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

HASHTAG = ""
NAME = "NAME"
TIME = "0"
PREV_NAME = "Name"
PREV_TIME = "0"
CHECK = 1

GPIO.setmode(GPIO.BOARD)


for tweet in api.user_timeline(user_id = "YOUR TWITTER ID", count = "1"):
        PREV_NAME = tweet.user.name
        PREV_TIME = tweet.created_at
        print (tweet.text)

def checkForTweets(pin):
        for tweet in api.user_timeline(user_id = "YOUR TWITTER ID", count = "1"):
                global CHANGED
                global NAME
                global TIME
                global PREV_NAME
                global PREV_TIME
                NAME = tweet.user.name
                TIME = tweet.created_at
                HASHTAG = tweet.entities.get('hashtags')
                DATETIME = datetime.datetime.strptime(str(TIME), "%Y-%m-%d %H:%M:%S")

                if ("ON" in tweet.text):
                        #print DATETIME
                        #print NAME
                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.output(pin,GPIO.LOW)
                        time.sleep(1)
                        print "LED OFF"

                        CHANGED=True
                else:
                        CHANGED =False

                PREV_NAME = NAME
                PREV_TIME = DATETIME

                if ("OFF" in tweet.text):
                        #print "CHANGED"
                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.output(pin,GPIO.HIGH)
                        time.sleep(1)
                        print "LED ON"

                        CHANGED = False


def checkForPressure(pin):

        reading = 0
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.2)

        GPIO.setup(pin, GPIO.IN)

        while(GPIO.input(pin) == GPIO.LOW):
                reading +=1
        print reading



        if reading > 3000:
                api.update_status(str(datetime.datetime.now().time()) + "ON" )
                time.sleep(5)
        elif reading < 3000:
                api.update_status(str(datetime.datetime.now().time()) + "OFF" )
                time.sleep(5)
while True:

        checkForTweets(7)
        checkForPressure(18)
        time.sleep(60)