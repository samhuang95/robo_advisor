# every year update the data score standar
import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv

now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
year = now.strftime("%Y")


df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
step_times_score = round(df['step_times'].sort_values(ascending=False)[:10].mean())
product_page_bounce_rate_score = round(df['product_page_bounce_rate'].sort_values(ascending=False)[:10].mean())
unique_visitors_score = round(df['unique_visitors'].sort_values(ascending=False)[:10].mean())
new_visitors_score = round(df['new_visitors'].sort_values(ascending=False)[:10].mean())
return_visitors_score = round(df['return_visitors'].sort_values(ascending=False)[:10].mean())
new_fans_score = round(df['new_fans'].sort_values(ascending=False)[:10].mean())
search_clicks_score = round(df['search_clicks'].sort_values(ascending=False)[:10].mean())
product_page_views_score = round(df['product_page_views'].sort_values(ascending=False)[:10].mean())
product_likes_score = round(df['product_likes'].sort_values(ascending=False)[:10].mean())

event_score_std = {
    'step_times_score': step_times_score,
    'product_page_bounce_rate_score': product_page_bounce_rate_score,
    'unique_visitors_score': unique_visitors_score,
    'new_visitors_score': new_visitors_score,
    'return_visitors_score': return_visitors_score,
    'new_fans_score': new_fans_score,
    'search_clicks_score': search_clicks_score,
    'product_page_views_score': product_page_views_score,
    'product_likes_score': product_likes_score
}

df = pd.DataFrame([event_score_std])
df.to_csv(f'./dataset/{year}_event_score_std.csv', index=False)


df = pd.read_csv(f'./dataset/noevent_data{yesterday}.csv', sep=',')
step_times_score = round(df['step_times'].sort_values(ascending=False)[:10].mean())
product_page_bounce_rate_score = round(df['product_page_bounce_rate'].sort_values(ascending=False)[:10].mean())
unique_visitors_score = round(df['unique_visitors'].sort_values(ascending=False)[:10].mean())
new_visitors_score = round(df['new_visitors'].sort_values(ascending=False)[:10].mean())
return_visitors_score = round(df['return_visitors'].sort_values(ascending=False)[:10].mean())
new_fans_score = round(df['new_fans'].sort_values(ascending=False)[:10].mean())
search_clicks_score = round(df['search_clicks'].sort_values(ascending=False)[:10].mean())
product_page_views_score = round(df['product_page_views'].sort_values(ascending=False)[:10].mean())
product_likes_score = round(df['product_likes'].sort_values(ascending=False)[:10].mean())

noevent_score_std = {
    'step_times_score': step_times_score,
    'product_page_bounce_rate_score': product_page_bounce_rate_score,
    'unique_visitors_score': unique_visitors_score,
    'new_visitors_score': new_visitors_score,
    'return_visitors_score': return_visitors_score,
    'new_fans_score': new_fans_score,
    'search_clicks_score': search_clicks_score,
    'product_page_views_score': product_page_views_score,
    'product_likes_score': product_likes_score
}

df = pd.DataFrame([noevent_score_std])
df.to_csv(f'./dataset/{year}_noevent_score_std.csv', index=False)






