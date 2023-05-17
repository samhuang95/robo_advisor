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
    if month == day and day == 18 and yesterday.weekday() == 2 and yesterday.weekday() == 2:
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
        print(reader)
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
        for noevent_weight in reader:
        # 將每一筆資料轉換成 dictionary
            feature = noevent_weight['feature']
            
            importance = noevent_weight['importance']
            
            weight_dict[feature] = importance
        
        # 獲取資料變數
    noevent_product_page_views = float(weight_dict['product_page_views'])
    # print(noevent_product_page_views)
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
    if month == day and day == 18 and yesterday.weekday() == 2:
        df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
        return {
            'AVG_step_times' : df['step_times'].mean(),
            'AVG_product_page_bounce_rate' : df['product_page_bounce_rate'].mean(),
            'AVG_unique_visitors' : df['unique_visitors'].mean(),
            'AVG_new_visitors' : df['new_visitors'].mean(),
            'AVG_return_visitors' : df['return_visitors'].mean(),
            'AVG_new_fans' : df['new_fans'].mean(),
            'AVG_search_clicks' : df['search_clicks'].mean(),
            'AVG_product_page_views' : df['product_page_views'].mean(),
            'AVG_product_likes' : df['product_likes'].mean()
        }
    else:
        df = pd.read_csv(f'./dataset/noevent_data{yesterday}.csv', sep=',')
        return {
            'AVG_step_times' : df['step_times'].mean(),
            'AVG_product_page_bounce_rate' : df['product_page_bounce_rate'].mean(),
            'AVG_unique_visitors' : df['unique_visitors'].mean(),
            'AVG_new_visitors' : df['new_visitors'].mean(),
            'AVG_return_visitors' : df['return_visitors'].mean(),
            'AVG_new_fans' : df['new_fans'].mean(),
            'AVG_search_clicks' : df['search_clicks'].mean(),
            'AVG_product_page_views' : df['product_page_views'].mean(),
            'AVG_product_likes' : df['product_likes'].mean()
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
    etw = event_training_weight()
    if month == day and day == 18 and yesterday.weekday() == 2:
        # data / mean * weight%
        return {
        'product_page_views' : dd['product_page_views'] / fm['AVG_product_page_views'] * etw['prop_event_product_page_views'],
        'step_times' : dd['step_times'] / fm['AVG_step_times'] * etw['prop_event_step_times'],
        'product_page_bounce_rate' : dd['product_page_bounce_rate'] / fm['AVG_product_page_bounce_rate'] * etw['prop_event_product_page_bounce_rate'],
        'unique_visitors' : dd['unique_visitors'] / fm['AVG_unique_visitors'] * etw['prop_event_unique_visitors'],
        'new_visitors' : dd['new_visitors'] / fm['AVG_new_visitors'] * etw['prop_event_new_visitors'],
        'return_visitors' : dd['return_visitors'] / fm['AVG_return_visitors'] * etw['prop_event_return_visitors'],
        'new_fans' : dd['new_fans'] / fm['AVG_new_fans'] * etw['prop_event_new_fans'],
        'search_clicks' : dd['search_clicks'] / fm['AVG_search_clicks'] * etw['prop_event_search_clicks'],
        'product_likes' : dd['product_likes'] / fm['AVG_product_likes'] * etw['prop_event_product_likes'],
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
    fm = feature_mean()
    dd = daily_data()

    if dd['product_page_views'] < fm['AVG_product_page_views']:
        product_page_views = abs(fm['AVG_product_page_views'] - dd['product_page_views'])
        insight_message['product_page_views'] = f"商品頁面瀏覽數低於每日平均 {product_page_views} 次"    
    
    if dd['step_times'] < fm['AVG_step_times']:
        step_times = abs(fm['AVG_step_times'] - dd['step_times'])
        insight_message['step_times'] = f"用戶停留時間低於每日平均 {step_times} 秒"
        
    if dd['product_page_bounce_rate'] > fm['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = abs(fm['AVG_product_page_bounce_rate'] - dd['product_page_bounce_rate'])
        insight_message['product_page_bounce_rate'] = f"用戶跳出率高於每日平均 {product_page_bounce_rate} %"

    if dd['unique_visitors'] < fm['AVG_unique_visitors']:
        unique_visitors = abs(fm['AVG_unique_visitors'] - dd['unique_visitors'])
        insight_message['unique_visitors'] = f"不重複拜訪用戶低於每日平均 {unique_visitors} 人次"

    if dd['new_visitors'] < fm['AVG_new_visitors']:
        new_visitors = abs(fm['AVG_new_visitors'] - dd['new_visitors'])
        insight_message['new_visitors'] = f"新拜訪用戶低於每日平均 {new_visitors} 人次"

    if dd['return_visitors'] < fm['AVG_return_visitors']:
        return_visitors = abs(fm['AVG_return_visitors'] - dd['return_visitors'])
        insight_message['return_visitors'] = f"回訪用戶低於每日平均 {return_visitors} 人次"

    if dd['new_fans'] < fm['AVG_new_fans']:
        new_fans = abs(fm['AVG_new_fans'] - dd['new_fans'])
        insight_message['new_fans'] = f"新加入粉絲低於每日平均 {new_fans} 人次"

    if dd['search_clicks'] < fm['AVG_search_clicks']:
        search_clicks = abs(fm['AVG_search_clicks'] - dd['search_clicks'])
        insight_message['search_clicks'] = f"搜尋點擊低於每日平均 {search_clicks} 次"

    if dd['product_likes'] < fm['AVG_product_likes']:
        product_likes = abs(fm['AVG_product_likes'] - dd['product_likes'])
        insight_message['product_likes'] = f"收藏點擊次數低於每日平均 {product_likes} 次"
# =========================================================================
    if dd['product_page_views'] > fm['AVG_product_page_views']:
        product_page_views = abs(fm['AVG_product_page_views'] - dd['product_page_views'])
        insight_message['product_page_views'] = f"商品頁面瀏覽數高於每日平均 {product_page_views} 次"    
    
    if dd['step_times'] > fm['AVG_step_times']:
        step_times = abs(fm['AVG_step_times'] - dd['step_times'])
        insight_message['step_times'] = f"用戶停留時間高於每日平均 {step_times} 秒"
        
    if dd['product_page_bounce_rate'] < fm['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = abs(fm['AVG_product_page_bounce_rate'] - dd['product_page_bounce_rate'])
        insight_message['product_page_bounce_rate'] = f"用戶跳出率低於每日平均 {product_page_bounce_rate} %"

    if dd['unique_visitors'] > fm['AVG_unique_visitors']:
        unique_visitors = abs(fm['AVG_unique_visitors'] - dd['unique_visitors'])
        insight_message['unique_visitors'] = f"不重複拜訪用戶高於每日平均 {unique_visitors} 人次"

    if dd['new_visitors'] > fm['AVG_new_visitors']:
        new_visitors = abs(fm['AVG_new_visitors'] - dd['new_visitors'])
        insight_message['new_visitors'] = f"新拜訪用戶高於每日平均 {new_visitors} 人次"

    if dd['return_visitors'] > fm['AVG_return_visitors']:
        return_visitors = abs(fm['AVG_return_visitors'] - dd['return_visitors'])
        insight_message['return_visitors'] = f"回訪用戶高於每日平均 {return_visitors} 人次"

    if dd['new_fans'] > fm['AVG_new_fans']:
        new_fans = abs(fm['AVG_new_fans'] - dd['new_fans'])
        insight_message['new_fans'] = f"新加入粉絲高於每日平均 {new_fans} 人次"

    if dd['search_clicks'] > fm['AVG_search_clicks']:
        search_clicks = abs(fm['AVG_search_clicks'] - dd['search_clicks'])
        insight_message['search_clicks'] = f"搜尋點擊高於每日平均 {search_clicks} 次"

    if dd['product_likes'] > fm['AVG_product_likes']:
        product_likes = abs(fm['AVG_product_likes'] - dd['product_likes'])
        insight_message['product_likes'] = f"收藏點擊次數高於每日平均 {product_likes} 次"
    
    return insight_message

insights = daily_insight()
print(insights['step_times'])
print('='*30)
print(insights)


# ----------------------------------------------------
def daily_score():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    # if month == day and day == 18 and yesterday.weekday() == 2:
    df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')      
    step_times_score = df['step_times'].sort_values(ascending=False)[:3].mean()
        # product_page_bounce_rate_score = df['product_page_bounce_rate'].mean()
        # unique_visitors_score = df['unique_visitors'].mean()
        # new_visitors_score = df['new_visitors'].mean()
        # return_visitors_score = df['return_visitors'].mean()
        # new_fans_score = df['new_fans'].mean()
        # search_clicks_score = df['search_clicks'].mean()
        # product_page_views_score = df['product_page_views'].mean()
        # product_likes_score = df['product_likes'].mean()


print('\n=====================')
dr = daily_report()
print(sum(dr.values()))
print('\n=====================')
print(dr['product_page_views'])



# 先找出何謂 100，標準應該要固定 
# 帶來最高業績那一天？
# 


# dr = daily_report()
# fm = feature_mean()

# print(dr['step_times'])
# print(fm['AVG_step_times'])

