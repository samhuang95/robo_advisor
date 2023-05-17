# every year update the data score standar
import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv

def daily_score():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    # if month == day and day == 18 and yesterday.weekday() == 2:
    df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
    return {
        'step_times_score' : round(df['step_times'].sort_values(ascending=False)[:3].mean()),
        'product_page_bounce_rate_score' : round(df['product_page_bounce_rate'].sort_values(ascending=False)[:3].mean()),
        'unique_visitors_score' : round(df['unique_visitors'].sort_values(ascending=False)[:3].mean()),
        'new_visitors_score' : round(df['new_visitors'].sort_values(ascending=False)[:3].mean()),
        'return_visitors_score' : round(df['return_visitors'].sort_values(ascending=False)[:3].mean()),
        'new_fans_score' : round(df['new_fans'].sort_values(ascending=False)[:3].mean()),
        'search_clicks_score' : round(df['search_clicks'].sort_values(ascending=False)[:3].mean()),
        'product_page_views_score' : round(df['product_page_views'].sort_values(ascending=False)[:3].mean()),
        'product_likes_score' : round(df['product_likes'].sort_values(ascending=False)[:3].mean())
    }

ds = daily_score()
print(ds)



