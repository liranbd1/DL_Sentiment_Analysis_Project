import pandas as pd
import matplotlib.pyplot as plt


train_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\train.csv")
test_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\test.csv")
valid_df = pd.read_csv("C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs\\valid.csv")

df_list = [train_df, test_df, valid_df]

word_count_dict = {}

for df in df_list:
    for idx, row in df.iterrows():
        if row['Word_Count'] not in word_count_dict.keys():
            word_count_dict[row['Word_Count']] = 1
        else:
            word_count_dict[row['Word_Count']] += 1

lists = sorted(word_count_dict.items())

x,y = zip(*lists)

total_count = 0
long_count = 0
for key in word_count_dict.keys():
    total_count += word_count_dict[key]
    if key > 35:
        long_count +=  word_count_dict[key]
         
print(total_count)
print(long_count)  
plt.bar(x,y)
plt.show()