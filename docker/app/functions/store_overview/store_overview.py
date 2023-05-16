# (V)1. 監控賣場經營分數(權重*當前數值，計算分數)
# (V)3. 銷售額、商品瀏覽數、訪客數、成交量   daily_report()
# (V)4. 當日 highlight

import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv
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
        'prop_noevent_product_likes' : noevent_product_likes / noevent_SUM * 100
        }


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
    dd = daily_data()
    fm = feature_mean()
    ntw = noevent_training_weight()
    if month == day and day == 18:
        # data / mean * weight%
        return {
        'product_page_views' : dd['product_page_views'] / fm['AVG_product_page_views'] * ntw['prop_noevent_product_page_views'],
        'step_times' : dd['step_times'] / fm['AVG_step_times'] * ntw['prop_noevent_step_times'],
        'product_page_bounce_rate' : dd['product_page_bounce_rate'] / fm['AVG_product_page_bounce_rate'] * ntw['prop_noevent_product_page_bounce_rate'],
        'unique_visitors' : dd['unique_visitors'] / fm['AVG_unique_visitors'] * ntw['prop_noevent_unique_visitors'],
        'new_visitors' : dd['new_visitors'] / fm['AVG_new_visitors'] * ntw['prop_noevent_new_visitors'],
        'return_visitors' : dd['return_visitors'] / fm['AVG_return_visitors'] * ntw['prop_noevent_return_visitors'],
        'new_fans' : dd['new_fans'] / fm['AVG_new_fans'] * ntw['prop_noevent_new_fans'],
        'search_clicks' : dd['search_clicks'] / fm['AVG_search_clicks'] * ntw['prop_noevent_search_clicks'],
        'product_likes' : dd['product_likes'] / fm['AVG_product_likes'] * ntw['prop_noevent_product_likes'],
        }
    else:
        return {
        'product_page_views' : dd['product_page_views'] / fm['AVG_product_page_views'] * ntw['prop_noevent_product_page_views'],
        'step_times' : dd['step_times'] / fm['AVG_step_times'] * ntw['prop_noevent_step_times'],
        'product_page_bounce_rate' : dd['product_page_bounce_rate'] / fm['AVG_product_page_bounce_rate'] * ntw['prop_noevent_product_page_bounce_rate'],
        'unique_visitors' : dd['unique_visitors'] / fm['AVG_unique_visitors'] * ntw['prop_noevent_unique_visitors'],
        'new_visitors' : dd['new_visitors'] / fm['AVG_new_visitors'] * ntw['prop_noevent_new_visitors'],
        'return_visitors' : dd['return_visitors'] / fm['AVG_return_visitors'] * ntw['prop_noevent_return_visitors'],
        'new_fans' : dd['new_fans'] / fm['AVG_new_fans'] * ntw['prop_noevent_new_fans'],
        'search_clicks' : dd['search_clicks'] / fm['AVG_search_clicks'] * ntw['prop_noevent_search_clicks'],
        'product_likes' : dd['product_likes'] / fm['AVG_product_likes'] * ntw['prop_noevent_product_likes'],
        }        

# ----------------------------------------------------
def daily_insight():
    # shopee events
    # 讀取有活動參與的數據
    insight_message = {}
    dr = daily_report()
    fm = feature_mean()
    if dr['product_page_views'] < fm['AVG_product_page_views']:
        product_page_views = fm['AVG_product_page_views'] - dr['product_page_views']
        insight_message['product_page_views'] = f"商品頁面瀏覽數低於每日平均{product_page_views}次"
    
    if dr['step_times'] < fm['AVG_step_times']:
        step_times = fm['AVG_step_times'] - dr['step_times']
        insight_message['step_times'] = f"用戶停留時間低於每日平均{step_times}秒"
        
    if dr['product_page_bounce_rate'] > fm['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = fm['AVG_product_page_bounce_rate'] - dr['product_page_bounce_rate']
        insight_message['product_page_bounce_rate'] = f"用戶跳出率高於每日平均{product_page_bounce_rate}%"

    if dr['unique_visitors'] < fm['AVG_unique_visitors']:
        unique_visitors = fm['AVG_unique_visitors'] - dr['unique_visitors']
        insight_message['unique_visitors'] = f"不重複拜訪用戶低於每日平均{unique_visitors}人次"

    if dr['new_visitors'] < fm['AVG_new_visitors']:
        new_visitors = fm['AVG_new_visitors'] - dr['new_visitors']
        insight_message['new_visitors'] = f"新拜訪用戶低於每日平均{new_visitors}人次"

    if dr['return_visitors'] < fm['AVG_return_visitors']:
        return_visitors = fm['AVG_return_visitors'] - dr['return_visitors']
        insight_message['return_visitors'] = f"回訪用戶低於每日平均{return_visitors}人次"

    if dr['new_fans'] < fm['AVG_new_fans']:
        new_fans = fm['AVG_new_fans'] - dr['new_fans']
        insight_message['new_fans'] = f"新加入粉絲低於每日平均{new_fans}人次"

    if dr['search_clicks'] < fm['AVG_search_clicks']:
        search_clicks = fm['AVG_search_clicks'] - dr['search_clicks']
        insight_message['search_clicks'] = f"搜尋點擊低於每日平均{search_clicks}次"

    if dr['product_likes'] < fm['AVG_product_likes']:
        product_likes = fm['AVG_product_likes'] - dr['product_likes']
        insight_message['product_likes'] = f"收藏點擊次數低於每日平均{product_likes}次"
    
    return insight_message


print(insight_message)



