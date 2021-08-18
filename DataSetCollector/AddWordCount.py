from numpy import nan
import pandas as pd
from pandas.io.parsers import read_csv

train_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\train.csv")
test_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\test.csv")
valid_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\valid.csv")

max_words = 0
df_list = [train_df, test_df, valid_df]
name_list = ["train", "test","valid" ]
for idx, df in enumerate(df_list):
    df.dropna(subset=['tweet'], inplace=True)
    len_list = []
    for index, row in df.iterrows():
        tweet_words = row['tweet'].split()
        if len(tweet_words) > 35:
            df.drop([index], inplace=True)
            continue
        len_list.append(len(tweet_words))
        if max_words<len_list[-1]:
            max_words = len_list[-1]
    df['Word_Count'] = len_list
    df.to_csv(f"C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\{name_list[idx]}.csv")


print(max_words)