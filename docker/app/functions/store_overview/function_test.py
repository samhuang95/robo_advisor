import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv
from store_overview import *

# def daily_score():
#     now = datetime.now()
#     yesterday = (now - timedelta(days=1)).date()
#     month = yesterday.strftime("%m")
#     day = yesterday.strftime("%d")
#     year = now.strftime("%Y")

#     dd = daily_data()
#     etw = event_training_weight()
#     ntw = noevent_training_weight()

#     if month == day and day == 18 and yesterday.weekday() == 2:
        
#         with open(f'./dataset/{year}_event_score_std.csv') as csvfile:
#             reader = csv.DictReader(csvfile, delimiter=',')
#             max_data = {}
#             for row in reader:
#                 for key, value in row.items():
#                     max_data[key] = int(value)
#         # 將數值縮放至 0~100 範圍內，然後 * weight %
#         return {
#             'product_page_views' : ((dd['product_page_views']) / (max_data['product_page_views_score'])) * 100 * etw['prop_event_product_page_views'],
#             'step_times' : ((dd['step_times']) / (max_data['step_times_score'])) * 100 * etw['prop_event_step_times'],
#             'product_page_bounce_rate' : ((dd['product_page_bounce_rate']) / (max_data['product_page_bounce_rate_score'])) * 100 * etw['prop_event_product_page_bounce_rate'],
#             'unique_visitors' : ((dd['unique_visitors']) / (max_data['unique_visitors_score'])) * 100 * etw['prop_event_unique_visitors'],
#             'new_visitors' : ((dd['new_visitors']) / (max_data['new_visitors_score'])) * 100 * etw['prop_event_new_visitors'],
#             'return_visitors' : ((dd['return_visitors']) / (max_data['return_visitors_score'])) * 100 * etw['prop_event_return_visitors'],
#             'new_fans' : ((dd['new_fans']) / (max_data['new_fans_score'])) * 100 * etw['prop_event_new_fans'],
#             'search_clicks' : ((dd['search_clicks']) / (max_data['search_clicks_score'])) * 100 * etw['prop_event_search_clicks'],
#             'product_likes' : ((dd['product_likes']) / (max_data['product_likes_score'])) * 100 * etw['prop_event_product_likes']
#             }
#     else:
        
#         with open(f'./dataset/{year}_noevent_score_std.csv') as csvfile:
#             reader = csv.DictReader(csvfile, delimiter=',')
#             max_data = {}
#             for row in reader:
#                 for key, value in row.items():
#                     max_data[key] = int(value)

#         # 將數值縮放至 0~100 範圍內，然後 * weight %
#         return {
#             'product_page_views' : ((dd['product_page_views']) / (max_data['product_page_views_score'])) * 100 * ntw['prop_noevent_product_page_views'],
#             'step_times' : ((dd['step_times']) / (max_data['step_times_score'])) * 100 * ntw['prop_noevent_step_times'],
#             'product_page_bounce_rate' : ((dd['product_page_bounce_rate']) / (max_data['product_page_bounce_rate_score'])) * 100 * ntw['prop_noevent_product_page_bounce_rate'],
#             'unique_visitors' : ((dd['unique_visitors']) / (max_data['unique_visitors_score'])) * 100 * ntw['prop_noevent_unique_visitors'],
#             'new_visitors' : ((dd['new_visitors']) / (max_data['new_visitors_score'])) * 100 * ntw['prop_noevent_new_visitors'],
#             'return_visitors' : ((dd['return_visitors']) / (max_data['return_visitors_score'])) * 100 * ntw['prop_noevent_return_visitors'],
#             'new_fans' : ((dd['new_fans']) / (max_data['new_fans_score'])) * 100 * ntw['prop_noevent_new_fans'],
#             'search_clicks' : ((dd['search_clicks']) / (max_data['search_clicks_score'])) * 100 * ntw['prop_noevent_search_clicks'],
#             'product_likes' : ((dd['product_likes']) / (max_data['product_likes_score'])) * 100 * ntw['prop_noevent_product_likes']
#             }

# ds = daily_score()

# print(ds['product_page_views'])



now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")
year = now.strftime("%Y")

dd = daily_data()
etw = event_training_weight()
ntw = noevent_training_weight()

with open(f'./dataset/{year}_event_score_std.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            max_data = {}
            for row in reader:
                for key, value in row.items():
                    max_data[key] = int(value)


dd = daily_data()
etw = event_training_weight()
ntw = noevent_training_weight()
product_page_views = ((dd['product_page_views']) / (max_data['product_page_views_score'])) * ntw['prop_noevent_product_page_views']

print(product_page_views)
print(dd['product_page_views'])
print(max_data['product_page_views_score'])
print(ntw['prop_noevent_product_page_views'])