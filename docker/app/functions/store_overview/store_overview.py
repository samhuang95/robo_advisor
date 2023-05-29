import configparser
import sys
# sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from ..connect_to_db import SQLcommand
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv
from sklearn.tree import DecisionTreeRegressor

# ----------------------------------------------------
def daily_data(time_select):
    print(time_select)
    time_select_dt = datetime.strptime(time_select, '%Y-%m-%d')
    month = time_select_dt.strftime("%m")
    day = time_select_dt.strftime("%d")

    # shopee events
    # 讀取有活動參與的數據
    if month == day or day == '18' or time_select_dt.weekday() == 2:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, 
            t.unique_visitors, t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time LIKE '{time_select}'
        GROUP BY 
            pd.date_time, t.date_time
        HAVING 
            MONTH(t.date_time) = DAY(t.date_time) OR 
            DAY(t.date_time) = 18 OR
            (DAYOFWEEK(t.date_time) = 4)
        ORDER BY 1 DESC;
            ''')
        return {
        'event_noevent_data' : df,
        'date_time' : df[0][0], 
        'product_page_views' : float(df[0][1]),
        'step_times' : float(df[0][2]),
        'product_page_bounce_rate' : float(df[0][3]),
        'unique_visitors' : float(df[0][4]),
        'new_visitors' : float(df[0][5]),
        'return_visitors' :float(df[0][6]),
        'new_fans' : float(df[0][7]),
        'search_clicks' : float(df[0][8]),
        'product_likes' : float(df[0][9]),
        'sale_products' : float(df[0][10]),
        'total_sales' :float(df[0][11])
        }

    else:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, t.unique_visitors, 
            t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time LIKE '{time_select}'
        GROUP BY
            pd.date_time, t.date_time
        HAVING
            (MONTH(t.date_time) <> DAY(t.date_time)) AND 
            (DAY(t.date_time) <> 18) AND
            (DAYOFWEEK(t.date_time) <> 4)
            ORDER BY 1 DESC;
            ''')
        # print(df)
        return {
        'event_noevent_data' : df,
        'date_time' : df[0][0], 
        'product_page_views' : float(df[0][1]),
        'step_times' : float(df[0][2]),
        'product_page_bounce_rate' : float(df[0][3]),
        'unique_visitors' : float(df[0][4]),
        'new_visitors' : float(df[0][5]),
        'return_visitors' :float(df[0][6]),
        'new_fans' : float(df[0][7]),
        'search_clicks' : float(df[0][8]),
        'product_likes' : float(df[0][9]),
        'sale_products' : float(df[0][10]),
        'total_sales' :float(df[0][11])
        }

    
# dd = daily_data('2023-05-28')
# print(dd['step_times'])

# ----------------------------------------------------
def feature_mean(time_select):
    time_select_dt = datetime.strptime(time_select, '%Y-%m-%d')
    month = time_select_dt.strftime("%m")
    day = time_select_dt.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    if month == day or day == '18' or time_select_dt.weekday() == 2:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, 
            t.unique_visitors, t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time <= '{time_select}'
        GROUP BY 
            pd.date_time, t.date_time
        HAVING 
            MONTH(t.date_time) = DAY(t.date_time) OR 
            DAY(t.date_time) = 18 OR
            (DAYOFWEEK(t.date_time) = 4)
        ORDER BY 1 DESC;
            ''')
        df = pd.DataFrame(df)
        all_data = {
        'product_page_views' : df[1].mean(),
        'step_times' : df[2].mean(),
        'product_page_bounce_rate' : df[3].mean(),
        'unique_visitors' : df[4].mean(),
        'new_visitors' : df[5].mean(),
        'return_visitors' :df[6].mean(),
        'new_fans' : df[7].mean(),
        'search_clicks' : df[8].mean(),
        'product_likes' : df[9].mean()
        }

    else:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, t.unique_visitors, 
            t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time <= '{time_select}'
        GROUP BY
            pd.date_time, t.date_time
        HAVING
            (MONTH(t.date_time) <> DAY(t.date_time)) AND 
            (DAY(t.date_time) <> 18) AND
            (DAYOFWEEK(t.date_time) <> 4)
            ORDER BY 1 DESC;
            ''')
        df = pd.DataFrame(df)
        all_data = {
        'product_page_views' : df[1].mean(),
        'step_times' : df[2].mean(),
        'product_page_bounce_rate' : df[3].mean(),
        'unique_visitors' : df[4].mean(),
        'new_visitors' : df[5].mean(),
        'return_visitors' :df[6].mean(),
        'new_fans' : df[7].mean(),
        'search_clicks' : df[8].mean(),
        'product_likes' : df[9].mean()
        }

    return {
        'AVG_step_times' : all_data['step_times'].mean(),
        'AVG_product_page_bounce_rate' : all_data['product_page_bounce_rate'].mean(),
        'AVG_unique_visitors' : all_data['unique_visitors'].mean(),
        'AVG_new_visitors' : all_data['new_visitors'].mean(),
        'AVG_return_visitors' : all_data['return_visitors'].mean(),
        'AVG_new_fans' : all_data['new_fans'].mean(),
        'AVG_search_clicks' : all_data['search_clicks'].mean(),
        'AVG_product_page_views' : all_data['product_page_views'].mean(),
        'AVG_product_likes' : all_data['product_likes'].mean()
        }

# fm = feature_mean('2023-05-28')
# print(fm['AVG_step_times'])
# # ---------------------------------------------------
def all_data(time_select):
    time_select_dt = datetime.strptime(time_select, '%Y-%m-%d')
    month = time_select_dt.strftime("%m")
    day = time_select_dt.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據
    if month == day or day == '18' or time_select_dt.weekday() == 2:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, 
            t.unique_visitors, t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time <= '{time_select}'
        GROUP BY 
            pd.date_time, t.date_time
        HAVING 
            MONTH(t.date_time) = DAY(t.date_time) OR 
            DAY(t.date_time) = 18 OR
            (DAYOFWEEK(t.date_time) = 4)
        ORDER BY 1 DESC;
            ''')
        return df

    else:
        df = SQLcommand().get(f'''
        SELECT 
            t.date_time, t.page_views AS product_page_views, 
            TIME_TO_SEC(t.time_on_page) AS step_times, 
            t.bounce_rate AS product_page_bounce_rate, t.unique_visitors, 
            t.new_visitors , t.return_visitors, t.new_fans, 
            SUM(pd.search_clicks) AS search_clicks, 
            SUM(pd.product_likes) AS product_likes, 
            SUM(pd.sale_products) AS sale_products,
            SUM(pd.total_sales) AS total_sales
        FROM 
            product_detail pd
                JOIN traffic_overview t
                    ON t.date_time = pd.date_time
        WHERE t.date_time <= '{time_select}'
        GROUP BY
            pd.date_time, t.date_time
        HAVING
            (MONTH(t.date_time) <> DAY(t.date_time)) AND 
            (DAY(t.date_time) <> 18) AND
            (DAYOFWEEK(t.date_time) <> 4)
            ORDER BY 1 DESC;
            ''')
        df = pd.DataFrame(df)
        return df

# ad = all_data('2023-05-28')
# print(ad)

# # ----------------------------------------------------
def daily_insight(time_select):
    # shopee events
    # 讀取有活動參與的數據
    insight_message = {}
    fm = feature_mean(time_select)
    dd = daily_data(time_select)

    if dd['product_page_views'] < fm['AVG_product_page_views']:
        product_page_views = round(abs(fm['AVG_product_page_views'] - dd['product_page_views']))
        insight_message['product_page_views'] = f"商品頁面瀏覽數低於每日平均 {product_page_views} 次"    

    if dd['step_times'] < fm['AVG_step_times']:
        step_times = round(abs(fm['AVG_step_times'] - dd['step_times']))
        insight_message['step_times'] = f"用戶停留時間低於每日平均 {step_times} 秒"

    if dd['product_page_bounce_rate'] > fm['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = round(abs(fm['AVG_product_page_bounce_rate'] - dd['product_page_bounce_rate']))
        insight_message['product_page_bounce_rate'] = f"用戶跳出率高於每日平均 {product_page_bounce_rate} %"

    if dd['unique_visitors'] < fm['AVG_unique_visitors']:
        unique_visitors = round(abs(fm['AVG_unique_visitors'] - dd['unique_visitors']))
        insight_message['unique_visitors'] = f"不重複拜訪用戶低於每日平均 {unique_visitors} 人次"

    if dd['new_visitors'] < fm['AVG_new_visitors']:
        new_visitors = round(abs(fm['AVG_new_visitors'] - dd['new_visitors']))
        insight_message['new_visitors'] = f"新拜訪用戶低於每日平均 {new_visitors} 人次"

    if dd['return_visitors'] < fm['AVG_return_visitors']:
        return_visitors = round(abs(fm['AVG_return_visitors'] - dd['return_visitors']))
        insight_message['return_visitors'] = f"回訪用戶低於每日平均 {return_visitors} 人次"

    if dd['new_fans'] < fm['AVG_new_fans']:
        new_fans = round(abs(fm['AVG_new_fans'] - dd['new_fans']))
        insight_message['new_fans'] = f"新加入粉絲低於每日平均 {new_fans} 人次"

    if dd['search_clicks'] < fm['AVG_search_clicks']:
        search_clicks = round(abs(fm['AVG_search_clicks'] - dd['search_clicks']))
        insight_message['search_clicks'] = f"搜尋點擊低於每日平均 {search_clicks} 次"

    if dd['product_likes'] < fm['AVG_product_likes']:
        product_likes = round(abs(fm['AVG_product_likes'] - dd['product_likes']))
        insight_message['product_likes'] = f"收藏點擊次數低於每日平均 {product_likes} 次"
# =========================================================================
    if dd['product_page_views'] > fm['AVG_product_page_views']:
        product_page_views = round(abs(fm['AVG_product_page_views'] - dd['product_page_views']))
        insight_message['product_page_views'] = f"商品頁面瀏覽數高於每日平均 {product_page_views} 次"    
    if dd['step_times'] > fm['AVG_step_times']:
        step_times = round(abs(fm['AVG_step_times'] - dd['step_times']))
        insight_message['step_times'] = f"用戶停留時間高於每日平均 {step_times} 秒"

    if dd['product_page_bounce_rate'] < fm['AVG_product_page_bounce_rate']:
        product_page_bounce_rate = round(abs(fm['AVG_product_page_bounce_rate'] - dd['product_page_bounce_rate']))
        insight_message['product_page_bounce_rate'] = f"用戶跳出率低於每日平均 {product_page_bounce_rate} %"

    if dd['unique_visitors'] > fm['AVG_unique_visitors']:
        unique_visitors = round(abs(fm['AVG_unique_visitors'] - dd['unique_visitors']))
        insight_message['unique_visitors'] = f"不重複拜訪用戶高於每日平均 {unique_visitors} 人次"

    if dd['new_visitors'] > fm['AVG_new_visitors']:
        new_visitors = round(abs(fm['AVG_new_visitors'] - dd['new_visitors']))
        insight_message['new_visitors'] = f"新拜訪用戶高於每日平均 {new_visitors} 人次"

    if dd['return_visitors'] > fm['AVG_return_visitors']:
        return_visitors = round(abs(fm['AVG_return_visitors'] - dd['return_visitors']))
        insight_message['return_visitors'] = f"回訪用戶高於每日平均 {return_visitors} 人次"

    if dd['new_fans'] > fm['AVG_new_fans']:
        new_fans = round(abs(fm['AVG_new_fans'] - dd['new_fans']))
        insight_message['new_fans'] = f"新加入粉絲高於每日平均 {new_fans} 人次"

    if dd['search_clicks'] > fm['AVG_search_clicks']:
        search_clicks = round(abs(fm['AVG_search_clicks'] - dd['search_clicks']))
        insight_message['search_clicks'] = f"搜尋點擊高於每日平均 {search_clicks} 次"

    if dd['product_likes'] > fm['AVG_product_likes']:
        product_likes = round(abs(fm['AVG_product_likes'] - dd['product_likes']))
        insight_message['product_likes'] = f"收藏點擊次數高於每日平均 {product_likes} 次"

    return insight_message

# di = daily_insight('2023-05-28')
# print(di)

# --------------------------------------------------------------
def feature_weight_model(time_select):

    df = all_data(time_select)
    df = pd.DataFrame(df)
    # 分離特徵和目標變量
    X = df.drop([0,10,11], axis=1)
    y = df[11]

    # 初始化決策樹回歸器
    model = DecisionTreeRegressor(random_state=0)

    # 訓練模型
    model.fit(X, y)

    # 獲取每個特徵的重要性得分
    importances = model.feature_importances_
    weight_dict = {}
    weight_column = ['product_page_views', 'step_times', 'product_page_bounce_rate', 'unique_visitors', 'new_visitors', 'return_visitors', 'new_fans', 'search_clicks', 'product_likes']
    for i in range(len(importances)):
        weight_dict[weight_column[i]] = importances[i]

    return {
        'product_page_views' : weight_dict['product_page_views'] / sum(weight_dict.values()) * 100,
        'step_times' : weight_dict['step_times'] / sum(weight_dict.values()) * 100,
        'product_page_bounce_rate' : weight_dict['product_page_bounce_rate'] / sum(weight_dict.values()) * 100,
        'unique_visitors' : weight_dict['unique_visitors'] / sum(weight_dict.values()) * 100,
        'new_visitors' : weight_dict['new_visitors'] / sum(weight_dict.values()) * 100,
        'return_visitors' : weight_dict['return_visitors'] / sum(weight_dict.values()) * 100,
        'new_fans' : weight_dict['new_fans'] / sum(weight_dict.values()) * 100,
        'search_clicks' : weight_dict['search_clicks'] / sum(weight_dict.values()) * 100,
        'product_likes' : weight_dict['product_likes'] / sum(weight_dict.values()) * 100
        }

# ff = feature_weight_model('2023-05-28')
# print(ff)

# ----------------------------------------------------
def daily_score(time_select):
    now = datetime.now()
    year = now.strftime("%Y")
    time_select_dt = datetime.strptime(time_select, '%Y-%m-%d')
    month = time_select_dt.strftime("%m")
    day = time_select_dt.strftime("%d")


    dd = daily_data(time_select)
    fwm = feature_weight_model(time_select)
    if month == day or day == '18' or time_select_dt.weekday() == 2:
        with open(f'/app/functions/store_overview/dataset/{year}_event_score_std.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            max_data = {}
            for row in reader:
                for key, value in row.items():
                    max_data[key] = int(value)
            
        # 將數值縮放至 0~100 範圍內，然後 * weight %
        score ={
            'product_page_views' : round(((dd['product_page_views']) / (max_data['product_page_views_score'])) * fwm['product_page_views']),
            'step_times' : round(((dd['step_times']) / (max_data['step_times_score'])) * fwm['step_times']),
            'product_page_bounce_rate' : round(((dd['product_page_bounce_rate']) / (max_data['product_page_bounce_rate_score'])) * fwm['product_page_bounce_rate']),
            'unique_visitors' : round(((dd['unique_visitors']) / (max_data['unique_visitors_score'])) * fwm['unique_visitors']),
            'new_visitors' : round(((dd['new_visitors']) / (max_data['new_visitors_score'])) * fwm['new_visitors']),
            'return_visitors' : round(((dd['return_visitors']) / (max_data['return_visitors_score'])) * fwm['return_visitors']),
            'new_fans' : round(((dd['new_fans']) / (max_data['new_fans_score'])) * fwm['new_fans']),
            'search_clicks' : round(((dd['search_clicks']) / (max_data['search_clicks_score'])) * fwm['search_clicks']),
            'product_likes' : round(((dd['product_likes']) / (max_data['product_likes_score'])) * fwm['product_likes'])
            }
        return sum(score.values())
    else:
        with open(f'/app/functions/store_overview/dataset/{year}_noevent_score_std.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            max_data = {}
            for row in reader:
                for key, value in row.items():
                    max_data[key] = int(value)
            
        # 將數值縮放至 0~100 範圍內，然後 * weight %
        score ={
            'product_page_views' : round(((dd['product_page_views']) / (max_data['product_page_views_score'])) * fwm['product_page_views']),
            'step_times' : round(((dd['step_times']) / (max_data['step_times_score'])) * fwm['step_times']),
            'product_page_bounce_rate' : round(((dd['product_page_bounce_rate']) / (max_data['product_page_bounce_rate_score'])) * fwm['product_page_bounce_rate']),
            'unique_visitors' : round(((dd['unique_visitors']) / (max_data['unique_visitors_score'])) * fwm['unique_visitors']),
            'new_visitors' : round(((dd['new_visitors']) / (max_data['new_visitors_score'])) * fwm['new_visitors']),
            'return_visitors' : round(((dd['return_visitors']) / (max_data['return_visitors_score'])) * fwm['return_visitors']),
            'new_fans' : round(((dd['new_fans']) / (max_data['new_fans_score'])) * fwm['new_fans']),
            'search_clicks' : round(((dd['search_clicks']) / (max_data['search_clicks_score'])) * fwm['search_clicks']),
            'product_likes' : round(((dd['product_likes']) / (max_data['product_likes_score'])) * fwm['product_likes'])
            }
        return sum(score.values())

# ds = daily_score('2023-05-28')
# print(ds)