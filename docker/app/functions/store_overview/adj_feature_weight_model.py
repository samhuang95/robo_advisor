from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import csv
from datetime import date, datetime, timedelta
import configparser
from adj_store_overview import daily_data
# ---------------------------------------------
# 【start to run the model and grap the weight values】

def feature_weight_model():
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).date()
    month = yesterday.strftime("%m")
    day = yesterday.strftime("%d")
    # shopee events
    # 讀取有活動參與的數據

    df = daily_data()
    df = df['event_noevent_data']
    data_list = list(df)

    df = pd.DataFrame(data_list, columns=[
        'date_time', 'product_page_views', 'step_times', 'product_page_bounce_rate', 'unique_visitors', 'new_visitors', 'return_visitors', 'new_fans', 'search_clicks', 'product_likes', 'sale_products', 'total_sales'
    ])

    # 分離特徵和目標變量
    X = df.drop(['sale_products','date_time', 'total_sales'], axis=1)
    y = df['sale_products']

    # 初始化決策樹回歸器
    model = DecisionTreeRegressor(random_state=0)

    # 訓練模型
    model.fit(X, y)

    # 獲取每個特徵的重要性得分
    importances = model.feature_importances_
    weight_dict = {}
    for i in range(len(importances)):
        weight_column = ['product_page_views', 'step_times', 'product_page_bounce_rate', 'unique_visitors', 'new_visitors', 'return_visitors', 'new_fans', 'search_clicks', 'product_likes']
        weight_dict[weight_column[i]] = importances[i]
    
    return {
        'prop_product_page_views' : weight_dict['product_page_views'] / sum(weight_dict.values()) * 100,
        'prop_step_times' : weight_dict['step_times'] / sum(weight_dict.values()) * 100,
        'prop_product_page_bounce_rate' : weight_dict['product_page_bounce_rate'] / sum(weight_dict.values()) * 100,
        'prop_unique_visitors' : weight_dict['unique_visitors'] / sum(weight_dict.values()) * 100,
        'prop_new_visitors' : weight_dict['new_visitors'] / sum(weight_dict.values()) * 100,
        'prop_return_visitors' : weight_dict['return_visitors'] / sum(weight_dict.values()) * 100,
        'prop_new_fans' : weight_dict['new_fans'] / sum(weight_dict.values()) * 100,
        'prop_search_clicks' : weight_dict['search_clicks'] / sum(weight_dict.values()) * 100,
        'prop_product_likes' : weight_dict['product_likes'] / sum(weight_dict.values()) * 100
        }

# fwm = feature_weight_model()
# print(fwm)

