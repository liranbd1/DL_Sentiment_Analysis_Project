import pandas as pd
import torch
df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\Anger.csv")

for idx, row in df.iterrows():
    if idx == 0:
        continue
    print(len(row['tweet']))