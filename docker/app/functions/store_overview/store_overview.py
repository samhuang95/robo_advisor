# (V)1. 監控賣場經營分數(權重*當前數值，計算分數)

# (V)3. 銷售額、商品瀏覽數、訪客數、成交量   daily_report()
# (V)4. 當日 highlight


import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv

config = configparser.ConfigParser()
config.read('config.ini')

# 設定連線資訊
config = {
    'user': config.get('store_overview', 'user'),
    'password': config.get('store_overview', 'password'),
    'host': config.get('store_overview', 'host'),
    'database': config.get('store_overview', 'database'),
    # 'ports': 
}

# 建立連線
cnx = mysql.connector.connect(**config)

# 建立 cursor
cursor = cnx.cursor()

# ----------------------------------------------------
def daily_data():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    if month == day and day == 18:
        df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
        return {   
        'product_page_views' : df.loc[df['date_time'] == f'{yesterday}', 'product_page_views'].values[0],
        'step_times' : df.loc[df['date_time'] == f'{yesterday}', 'step_times'].values[0],
        'product_page_bounce_rate' : df.loc[df['date_time'] == f'{yesterday}', 'product_page_bounce_rate'].values[0],
        'unique_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'unique_visitors'].values[0],
        'new_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'new_visitors'].values[0],
        'return_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'return_visitors'].values[0],
        'new_fans' : df.loc[df['date_time'] == f'{yesterday}', 'new_fans'].values[0],
        'search_clicks' : df.loc[df['date_time'] == f'{yesterday}', 'search_clicks'].values[0],
        'product_likes' : df.loc[df['date_time'] == f'{yesterday}', 'product_likes'].values[0],
        'sale_products' : df.loc[df['date_time'] == f'{yesterday}', 'sale_products'].values[0],
        'total_sales' : df.loc[df['date_time'] == f'{yesterday}', 'total_sales'].values[0]}
    else:
        df = pd.read_csv(f'./dataset/noevent_data{yesterday}.csv', sep=',')     
        return {   
        'product_page_views' : df.loc[df['date_time'] == f'{yesterday}', 'product_page_views'].values[0],
        'step_times' : df.loc[df['date_time'] == f'{yesterday}', 'step_times'].values[0],
        'product_page_bounce_rate' : df.loc[df['date_time'] == f'{yesterday}', 'product_page_bounce_rate'].values[0],
        'unique_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'unique_visitors'].values[0],
        'new_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'new_visitors'].values[0],
        'return_visitors' : df.loc[df['date_time'] == f'{yesterday}', 'return_visitors'].values[0],
        'new_fans' : df.loc[df['date_time'] == f'{yesterday}', 'new_fans'].values[0],
        'search_clicks' : df.loc[df['date_time'] == f'{yesterday}', 'search_clicks'].values[0],
        'product_likes' : df.loc[df['date_time'] == f'{yesterday}', 'product_likes'].values[0],
        'sale_products' : df.loc[df['date_time'] == f'{yesterday}', 'sale_products'].values[0],
        'total_sales' : df.loc[df['date_time'] == f'{yesterday}', 'total_sales'].values[0]}

# ----------------------------------------------------
def event_training_weight():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    # 讀取有活動的權重
    with open(f'./dataset/event_weight{yesterday}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        weight_dict = {}
        for event_weight in reader:
        # 將每一筆資料轉換成 dictionary
            feature = event_weight['feature']
            importance = event_weight['importance']
            weight_dict[feature] = importance
        event_product_page_views = float(weight_dict['product_page_views'])
        event_step_times = float(weight_dict['step_times'])
        event_product_page_bounce_rate = float(weight_dict['product_page_bounce_rate'])
        event_unique_visitors = float(weight_dict['unique_visitors'])
        event_new_visitors = float(weight_dict['new_visitors'])
        event_return_visitors = float(weight_dict['return_visitors'])
        event_new_fans = float(weight_dict['new_fans'])
        event_search_clicks = float(weight_dict['search_clicks'])
        event_product_likes = float(weight_dict['product_likes'])
        
        event_SUM = event_product_page_views + event_step_times + event_product_page_bounce_rate + event_unique_visitors + event_new_visitors + event_return_visitors + event_new_fans + event_search_clicks + event_product_likes
        
        return {
        'prop_event_product_page_views' : event_product_page_views / event_SUM * 100,
        'prop_event_step_times' : event_step_times / event_SUM * 100,
        'prop_event_product_page_bounce_rate' : event_product_page_bounce_rate / event_SUM * 100,
        'prop_event_unique_visitors' : event_unique_visitors / event_SUM * 100,
        'prop_event_new_visitors' : event_new_visitors / event_SUM * 100,
        'prop_event_return_visitors' : event_return_visitors / event_SUM * 100,
        'prop_event_new_fans' : event_new_fans / event_SUM * 100,
        'prop_event_search_clicks' : event_search_clicks / event_SUM * 100,
        'prop_event_product_likes' : event_product_likes / event_SUM * 100}

# event_training_weight_TT = event_training_weight()
# print(event_training_weight_TT)

# ----------------------------------------------------

def noevent_training_weight():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    # 讀取沒有活動的權重
    with open(f'./dataset/noevent_weight{yesterday}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        weight_dict = {}
        for event_weight in reader:
        # 將每一筆資料轉換成 dictionary
            feature = event_weight['feature']
            importance = event_weight['importance']
            weight_dict[feature] = importance
        # 獲取資料變數
        noevent_product_page_views = float(weight_dict['product_page_views'])
        noevent_step_times = float(weight_dict['step_times'])
        noevent_product_page_bounce_rate = float(weight_dict['product_page_bounce_rate'])
        noevent_unique_visitors = float(weight_dict['unique_visitors'])
        noevent_new_visitors = float(weight_dict['new_visitors'])
        noevent_return_visitors = float(weight_dict['return_visitors'])
        noevent_new_fans = float(weight_dict['new_fans'])
        noevent_search_clicks = float(weight_dict['search_clicks'])
        noevent_product_likes = float(weight_dict['product_likes'])

        noevent_SUM = noevent_product_page_views + noevent_step_times + noevent_product_page_bounce_rate + noevent_unique_visitors + noevent_new_visitors + noevent_return_visitors + noevent_new_fans + noevent_search_clicks + noevent_product_likes
        
        return {
        'prop_noevent_product_page_views' : noevent_product_page_views / noevent_SUM * 100,
        'prop_noevent_step_times' : noevent_step_times / noevent_SUM * 100,
        'prop_noevent_product_page_bounce_rate' : noevent_product_page_bounce_rate / noevent_SUM * 100,
        'prop_noevent_unique_visitors' : noevent_unique_visitors / noevent_SUM * 100,
        'prop_noevent_new_visitors' : noevent_new_visitors / noevent_SUM * 100,
        'prop_noevent_return_visitors' : noevent_return_visitors / noevent_SUM * 100,
        'prop_noevent_new_fans' : noevent_new_fans / noevent_SUM * 100,
        'prop_noevent_search_clicks' : noevent_search_clicks / noevent_SUM * 100,
        'prop_noevent_product_likes' : noevent_product_likes / noevent_SUM * 100}
    
 
# noevent_training_weight_TT = noevent_training_weight()
# print(noevent_training_weight_TT)

# ----------------------------------------------------
def feature_mean():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    if month == day and day == 18:
        df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
        return {
            'AVG_step_times' : df['step_times'] / len(df['step_times']),
            'AVG_product_page_bounce_rate' : df['AVG_product_page_bounce_rate'] / len(df['AVG_product_page_bounce_rate']),
            'AVG_unique_visitors' : df['AVG_unique_visitors'] / len(df['AVG_unique_visitors']),
            'AVG_new_visitors' : df['AVG_new_visitors'] / len(df['AVG_new_visitors']),
            'AVG_return_visitors' : df['AVG_return_visitors'] / len(df['AVG_return_visitors']),
            'AVG_new_fans' : df['AVG_new_fans'] / len(df['AVG_new_fans']),
            'AVG_search_clicks' : df['AVG_search_clicks'] / len(df['AVG_search_clicks']),
            'AVG_product_page_views' : df['AVG_product_page_views'] / len(df['AVG_product_page_views']),
            'AVG_product_likes' : df['AVG_product_likes'] / len(df['AVG_product_likes'])
        }
    else:
        df = pd.read_csv(f'./dataset/noevent_data{yesterday}.csv', sep=',')
        return {
            'AVG_step_times' : df['step_times'] / len(df['step_times']),
            'AVG_product_page_bounce_rate' : df['AVG_product_page_bounce_rate'] / len(df['AVG_product_page_bounce_rate']),
            'AVG_unique_visitors' : df['AVG_unique_visitors'] / len(df['AVG_unique_visitors']),
            'AVG_new_visitors' : df['AVG_new_visitors'] / len(df['AVG_new_visitors']),
            'AVG_return_visitors' : df['AVG_return_visitors'] / len(df['AVG_return_visitors']),
            'AVG_new_fans' : df['AVG_new_fans'] / len(df['AVG_new_fans']),
            'AVG_search_clicks' : df['AVG_search_clicks'] / len(df['AVG_search_clicks']),
            'AVG_product_page_views' : df['AVG_product_page_views'] / len(df['AVG_product_page_views']),
            'AVG_product_likes' : df['AVG_product_likes'] / len(df['AVG_product_likes'])
        }

# ----------------------------------------------------
def daily_report():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    if month == day and day == 18:
        # data / mean * weight%
        return {
        'product_page_views' : daily_data()['product_page_views'] / feature_mean()['AVG_product_page_views'] * noevent_training_weight()['prop_noevent_product_page_views'],
        'step_times' : daily_data()['step_times'] / feature_mean()['AVG_step_times'] * noevent_training_weight()['prop_noevent_step_times'],
        'product_page_bounce_rate' : daily_data()['product_page_bounce_rate'] / feature_mean()['AVG_product_page_bounce_rate'] * noevent_training_weight()['prop_noevent_product_page_bounce_rate'],
        'unique_visitors' : daily_data()['unique_visitors'] / feature_mean()['AVG_unique_visitors'] * noevent_training_weight()['prop_noevent_unique_visitors'],
        'new_visitors' : daily_data()['new_visitors'] / feature_mean()['AVG_new_visitors'] * noevent_training_weight()['prop_noevent_new_visitors'],
        'return_visitors' : daily_data()['return_visitors'] / feature_mean()['AVG_return_visitors'] * noevent_training_weight()['prop_noevent_return_visitors'],
        'new_fans' : daily_data()['new_fans'] / feature_mean()['AVG_new_fans'] * noevent_training_weight()['prop_noevent_new_fans'],
        'search_clicks' : daily_data()['search_clicks'] / feature_mean()['AVG_search_clicks'] * noevent_training_weight()['prop_noevent_search_clicks'],
        'product_likes' : daily_data()['product_likes'] / feature_mean()['AVG_product_likes'] * noevent_training_weight()['prop_noevent_product_likes'],
        }
    else:
        return {
        'product_page_views' : daily_data()['product_page_views'] / feature_mean()['AVG_product_page_views'] * noevent_training_weight()['prop_noevent_product_page_views'],
        'step_times' : daily_data()['step_times'] / feature_mean()['AVG_step_times'] * noevent_training_weight()['prop_noevent_step_times'],
        'product_page_bounce_rate' : daily_data()['product_page_bounce_rate'] / feature_mean()['AVG_product_page_bounce_rate'] * noevent_training_weight()['prop_noevent_product_page_bounce_rate'],
        'unique_visitors' : daily_data()['unique_visitors'] / feature_mean()['AVG_unique_visitors'] * noevent_training_weight()['prop_noevent_unique_visitors'],
        'new_visitors' : daily_data()['new_visitors'] / feature_mean()['AVG_new_visitors'] * noevent_training_weight()['prop_noevent_new_visitors'],
        'return_visitors' : daily_data()['return_visitors'] / feature_mean()['AVG_return_visitors'] * noevent_training_weight()['prop_noevent_return_visitors'],
        'new_fans' : daily_data()['new_fans'] / feature_mean()['AVG_new_fans'] * noevent_training_weight()['prop_noevent_new_fans'],
        'search_clicks' : daily_data()['search_clicks'] / feature_mean()['AVG_search_clicks'] * noevent_training_weight()['prop_noevent_search_clicks'],
        'product_likes' : daily_data()['product_likes'] / feature_mean()['AVG_product_likes'] * noevent_training_weight()['prop_noevent_product_likes'],
        }        

# ----------------------------------------------------
def daily_insight():
    # shopee events
    # 讀取有活動參與的數據
    insight_message = {}
    if daily_report()['product_page_views'] < feature_mean()['AVG_product_page_views']:
        product_page_views = feature_mean()['AVG_product_page_views'] - daily_report()['product_page_views']
        insight_message['product_page_views'] = f"商品頁面瀏覽數低於每日平均{product_page_views}次"
    
    if daily_report()['step_times'] < feature_mean()['AVG_step_times']:
        step_times = feature_mean()['AVG_step_times'] - daily_report()['step_times']
        insight_message['step_times'] = f"用戶停留時間低於每日平均{step_times}秒"
        
    if daily_report()['product_page_bounce_rate'] > feature_mean()['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = feature_mean()['AVG_product_page_bounce_rate'] - daily_report()['product_page_bounce_rate']
        insight_message['product_page_bounce_rate'] = f"用戶跳出率高於每日平均{product_page_bounce_rate}%"

    if daily_report()['unique_visitors'] < feature_mean()['AVG_unique_visitors']:
        unique_visitors = feature_mean()['AVG_unique_visitors'] - daily_report()['unique_visitors']
        insight_message['unique_visitors'] = f"不重複拜訪用戶低於每日平均{unique_visitors}人次"

    if daily_report()['new_visitors'] < feature_mean()['AVG_new_visitors']:
        new_visitors = feature_mean()['AVG_new_visitors'] - daily_report()['new_visitors']
        insight_message['new_visitors'] = f"新拜訪用戶低於每日平均{new_visitors}人次"

    if daily_report()['return_visitors'] < feature_mean()['AVG_return_visitors']:
        return_visitors = feature_mean()['AVG_return_visitors'] - daily_report()['return_visitors']
        insight_message['return_visitors'] = f"回訪用戶低於每日平均{return_visitors}人次"

    if daily_report()['new_fans'] < feature_mean()['AVG_new_fans']:
        new_fans = feature_mean()['AVG_new_fans'] - daily_report()['new_fans']
        insight_message['new_fans'] = f"新加入粉絲低於每日平均{new_fans}人次"

    if daily_report()['search_clicks'] < feature_mean()['AVG_search_clicks']:
        search_clicks = feature_mean()['AVG_search_clicks'] - daily_report()['search_clicks']
        insight_message['search_clicks'] = f"搜尋點擊低於每日平均{search_clicks}次"

    if daily_report()['product_likes'] < feature_mean()['AVG_product_likes']:
        product_likes = feature_mean()['AVG_product_likes'] - daily_report()['product_likes']
        insight_message['product_likes'] = f"收藏點擊次數低於每日平均{product_likes}次"
    
    return insight_message 

# 關閉 cursor 和連線
cursor.close()
cnx.close()