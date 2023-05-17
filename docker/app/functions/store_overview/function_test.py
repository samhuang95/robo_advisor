import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')        
step_times_score = df['step_times'].sort_values(ascending=False)[:3].mean()

print(step_times_score) # 110
