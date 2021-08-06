import os
import pandas as pd
csv_path ='C:\\Users\\liranb\\Desktop\\Sentiment Analysis - DL Final Project\\Dataset csvs'


for csv_file in os.listdir(csv_path):
    file_p = os.path.join(csv_path,csv_file)
    df = pd.read_csv(file_p)
    print(df.columns)
    label = df['label'][0]
    print(label)