#!/usr/bin/env python3

import markovify
import twitter
import csv
import re
import os

PATH_TO_MODEL   = '/tweets/model.json'
PATH_TO_TWEETS  = '/tweets/tweets.csv'
PATH_TO_SECRETS = '/secrets'

def make_model():
    with open(PATH_TO_TWEETS) as f:
        lines = []

        for tweet in csv.DictReader(f):
            # "tweet_id","in_reply_to_status_id","in_reply_to_user_id","timestamp","source","text",
            # "retweeted_status_id","retweeted_status_user_id","retweeted_status_timestamp","expanded_urls"
            if not tweet['in_reply_to_status_id'] and not tweet['retweeted_status_id']:
                scrubbed_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet['text'], flags=re.MULTILINE)
                scrubbed_tweet = scrubbed_tweet.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                lines.append(scrubbed_tweet)

        model = markovify.NewlineText("\n".join(lines))

        with open(PATH_TO_MODEL, 'wb') as f:
            f.write(model.to_json().encode('utf-8'))

def tweet(text):
    consumer_key        = 'ueIHhQOMuYdQ2jgbWNJ0nllpQ'
    access_token_key    = '85117657-Lpfqzxr0H6jyk83zm5S2ChfBcpwdmIPvqtOPP1bO0'
    username            = os.environ['TWITTER_USERNAME']

    with open(PATH_TO_SECRETS) as f:
        consumer_secret, access_token_secret = map(str.strip, f.read().strip().split("\n"))

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)

    api.PostUpdate(text)

if __name__ == "__main__":
    if not os.path.exists(PATH_TO_MODEL):
        make_model()

    with open(PATH_TO_MODEL, 'rb') as f:
        model = markovify.NewlineText.from_json(f.read().decode('utf-8'))

    text = model.make_short_sentence(280)
    print(text)
    tweet(text)

# https://github.com/jsvine/markovify
# https://github.com/bear/python-twitter