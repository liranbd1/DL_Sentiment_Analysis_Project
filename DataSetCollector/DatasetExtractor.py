from logging import captureWarnings, currentframe
import os
import tweepy as tw
import pandas as pd
import demoji
import re
from rootpath import ROOT_PATH
import glob

url_pattern = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'

start_date = "2021-1-1"
num_of_tweets = 1750
filter_list = [
    " -filter:retweets", # Filter out retweets
    " -filter:native_video", # Filter out twitts with videos
    " -filter:links", # Filter out twitts with URLs in them , Not sure this is good for us
]

tweets_pulled = 0
def set_tweets_pulled(value):
    global tweets_pulled
    tweets_pulled = value

categories_index = {
    "Anger": 0,
    "Hate": 1,
    "Happiness" : 2,
    "Love" : 3,
    "Supprised": 4,
    "Saddness": 5,
    "Depression": 6
}

''' 
Looking only by a category won't give us a lot of information, so we added a list of words that are connected to the category to search for.
This scenario will will be more helpful to aviod a twit bots that use the more general form of the word and can give us a more intreasting range 
on the category.
Only 3 more seacrch words for each category total 4 search words per category 
'''
search_words_by_category = {
    "Anger": ["annoyance", "angry", "annoyed", "anger"],
    "Hate": ["loathe", "dislike","hate", "hating"],
    "Happiness" : ["Happiness", "pleasure", "joy", "happy"],
    "Love" : ["love", "passion", "caring","cherish"],
    "Supprised": ["supprised", "amazed", "speechless", "dazed"],
    "Sadness": ["sadness", "sorrow", "misery", "down"],
    "Depression": ["depression", "melancholy", "depressed","gloom"]
}



class TwitterAPIAccess():

    class _TwitterAPIAccess():

        def __init__(self):
             
            consumer_key = "lnfeL7GP1tsoCXc6meR6TAFhv"
            consumer_key_secret = "apBc4UwTR95K7lvZxcrFs2VusnCQvpVAIRRNXqd8NvAu4xFuqg"
            access_token = "1064375574-l1hMnwU5C2gXs4urEzEw0oSktxPeZaJI9TREgWc"
            access_token_secret = "tYtZxibMFfDUMEpWVQ3ig7qWX3jtG72Wle265hOyQmyUe"
            self.auth = self.AuthorizeAccess(consumer_key, consumer_key_secret, access_token, access_token_secret)
            self.api = self.APIAccess()

        def AuthorizeAccess(self, key, key_secret, token, token_secret):
            auth = tw.OAuthHandler(key, key_secret)
            auth.set_access_token(token, token_secret)
            return auth
        
        def APIAccess(self):
            return tw.API(self.auth, wait_on_rate_limit=True)
    
    instance = None
    
    def __new__(self):
        if not TwitterAPIAccess.instance:
            TwitterAPIAccess.instance = TwitterAPIAccess._TwitterAPIAccess()
        
        return TwitterAPIAccess.instance.api

def add_filters(search_word):
    filtered_search = search_word
    for filter in filter_list:
        filtered_search += " AND" + filter
    
    return filtered_search

def SearchTwitter(search_word, api):
    print("Start search...")
    search_word = add_filters(search_word)
    tweets = tw.Cursor(api.search,
                        q= search_word,
                        lang = 'en',
                        since=start_date).items(num_of_tweets)
    print("Completed search...")
    tweet_list = [tweet.text for tweet in tweets]
    print(f"Total tweets: {len(tweet_list)}")
    set_tweets_pulled(len(tweet_list))
    return tweet_list

def ProcessTweest(tweets):
    processed_tweets = []
    #count = 0
    for tweet in tweets:
        # Using emojis description - Gives more info
        emoji_to_decription = demoji.replace_with_desc(tweet, sep=" ")
        # Removing mentions of other users or groups not relevant
        remove_mentions = re.sub('@[A-Za-z]*', " ", emoji_to_decription, flags=re.I)
        # Removing URLS from the tweet

        urls_in_tweet = re.findall(url_pattern, remove_mentions)
        clean_urls = remove_mentions
        for match in urls_in_tweet:
            url = match[0]
            clean_urls = clean_urls.replace(url, '')
        # Removes extra spaces in start and end

        clean_extra_spaces = clean_urls.strip()
        # Cleaning the # from the hashtags to use them as words

        clean_tweet = re.sub('[^a-zA-Z0-9 \.]', "", clean_extra_spaces, flags=re.I)
        if clean_tweet not in processed_tweets:
            processed_tweets.append(clean_tweet)
        #count += 1
        #print(f"Completed: {count*100/tweets_pulled} % ")
    print("Finished Processing...")
    print(f"Processed {len(processed_tweets)} tweets")
    return processed_tweets

def CreateCategoryTweets(category_search_words, api):
    clean_tweets_final = []
    for word in category_search_words:
        print(word)
        tweets = SearchTwitter(word, api)
        clean_tweets = ProcessTweest(tweets)
        for tweet in clean_tweets:
            clean_tweets_final.append(tweet)
    return set(clean_tweets_final)

def CreateDataset():
    api = TwitterAPIAccess()
    for category in search_words_by_category.keys():
        print(category)
        tweets = CreateCategoryTweets(search_words_by_category[category], api)
        print(f"Number of tweets {len(tweets)}")
        print("---"*10)
        tweets_cat = [[tweet, category] for tweet in tweets]
        tweet_pd = pd.DataFrame(data=tweets_cat, columns=['tweet', 'label'])
        tweet_pd.to_csv(path_or_buf=f'C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\{category}.csv')        

def Combine_CSVs():
    # 1) For each csv file in Dataset csvs folder combine them to one dataframe
    # 2) Shuffle the dataframe 
    # 3) Export 70-15-15 to 3 other csvs 
    train_list = []
    test_list = []
    valid_list = []
    csv_path ='C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs'
    for csv_file in os.listdir(csv_path):
        file_p = os.path.join(csv_path,csv_file)
        df = pd.read_csv(file_p)
        df_size = len(df.index)
        label = df['label'][0]
        train_size = int(0.7*df_size)
        rest_size = int(0.15*df_size)
        train_df = [[label,tweet] for tweet in df['tweet'][0:train_size]]
        test_df = [[label, tweet] for tweet in df['tweet'][train_size+1:train_size+rest_size+1]]
        valid_df = [[label, tweet] for tweet in df['tweet'][train_size+rest_size+2:]] 
        train_list += [k for k in train_df]
        test_list += [k for k in test_df]
        valid_list += [k for k in valid_df]

    train_DF = pd.DataFrame(train_list, columns=['label', 'tweet']).to_csv(f'{csv_path}\\train.csv')
    valid_DF = pd.DataFrame(valid_list, columns=['label', 'tweet']).to_csv(f'{csv_path}\\valid.csv')
    test_DF = pd.DataFrame(test_list, columns=['label', 'tweet']).to_csv(f'{csv_path}\\test.csv')

CreateDataset()

Combine_CSVs()
