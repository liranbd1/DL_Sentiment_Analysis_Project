from DatasetExtractor import TwitterAPIAccess
import tweepy as tw

api = TwitterAPIAccess()

search_word = "Hate"
tweets = tw.Cursor(api.search,
                    q= search_word,
                    lang = 'en',
                    since='1-1-2021').items(10)

for tweet in tweets:
    print(tweet.text)