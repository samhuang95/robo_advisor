from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import configparser

# 【create a new table for model training】
# connetion with MySQL
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

# 使用 SQL 查詢，取得活動日數據結果
event_sql = '''
SELECT 
    t.date_time,
    t.page_views AS product_page_views, 
    TIME_TO_SEC(t.time_on_page) AS step_times, 
    t.bounce_rate AS product_page_bounce_rate, 
    t.unique_visitors, 
    t.new_visitors , 
    t.return_visitors, 
    t.new_fans, 
    SUM(pd.search_clicks) AS search_clicks, 
    SUM(pd.product_likes) AS product_likes, 
    SUM(pd.sale_products) AS sale_products,
    SUM(pd.total_sales) AS total_sales
FROM 
    traffic_overview t
	    JOIN product_detail pd
		    ON t.date_time = pd.date_time
GROUP BY 
    pd.date_time, t.date_time
HAVING 
    MONTH(t.date_time) = DAY(t.date_time) OR 
    DAY(t.date_time) = 18 OR
    (DAYOFWEEK(t.date_time) = 4);'''
result = pd.read_sql(event_sql, cnx)

# 將結果轉成 DataFrame，並儲存下來
df = pd.DataFrame(result)
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
df.to_csv(f'./dataset/event_data{yesterday}.csv', index=False)

# --------------------------------------------------
# 使用 SQL 查詢，取得非活動日數據結果
event_sql = '''
SELECT 
    t.date_time,
    t.page_views AS product_page_views, 
    TIME_TO_SEC(t.time_on_page) AS step_times, 
    t.bounce_rate AS product_page_bounce_rate, 
    t.unique_visitors, 
    t.new_visitors , 
    t.return_visitors, 
    t.new_fans, 
    SUM(pd.search_clicks) AS search_clicks, 
    SUM(pd.product_likes) AS product_likes, 
    SUM(pd.sale_products) AS sale_products,
    SUM(pd.total_sales) AS total_sales
FROM 
    traffic_overview t
	    JOIN product_detail pd
		    ON t.date_time = pd.date_time
GROUP BY
    pd.date_time, t.date_time
HAVING
    (MONTH(t.date_time) <> DAY(t.date_time)) AND 
    (DAY(t.date_time) <> 18) AND
    (DAYOFWEEK(t.date_time) <> 4);'''
result = pd.read_sql(event_sql, cnx)

# 將結果轉成 DataFrame，並儲存下來
df = pd.DataFrame(result)
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
df.to_csv(f'./dataset/noevent_data{yesterday}.csv', index=False)

# 關閉 cursor 和連線
cursor.close()
cnx.close()
# ---------------------------------------------
# 【start to run the model and grap the weight values】

# 讀取沒有活動參與的數據
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
df = pd.read_csv(f'./dataset/noevent_data{yesterday}.csv', sep=',')
# print(df.head())
# 分離特徵和目標變量
X = df.drop(['sale_products','date_time', 'total_sales'], axis=1)
y = df['sale_products']

# 初始化決策樹回歸器
model = DecisionTreeRegressor(random_state=0)

# 訓練模型
model.fit(X, y)

# 獲取每個特徵的重要性得分
importances = model.feature_importances_

# 匯出每個特徵的重要性得分
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
with open(f'./dataset/noevent_weight{yesterday}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['feature', 'importance'])
    for feature, importance in zip(X.columns, importances):
        writer.writerow([feature, importance])
        print(f'{feature}: {importance}')

print(f'完成匯出 noevent_weight {yesterday}數據')
# ---------------------------------------------
# 讀取有活動參與的數據
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
df = pd.read_csv(f'./dataset/event_data{yesterday}.csv', sep=',')
# print(df.head())
# 分離特徵和目標變量
X = df.drop(['sale_products','date_time', 'total_sales'], axis=1)
y = df['sale_products']

# 初始化決策樹回歸器
model = DecisionTreeRegressor(random_state=0)

# 訓練模型
model.fit(X, y)

# 獲取每個特徵的重要性得分
importances = model.feature_importances_

# 匯出每個特徵的重要性得分
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
with open(f'./dataset/event_weight{yesterday}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['feature', 'importance'])
    for feature, importance in zip(X.columns, importances):
        writer.writerow([feature, importance])
        print(f'{feature}: {importance}')

print(f'完成匯出 event_weight {yesterday}數據')