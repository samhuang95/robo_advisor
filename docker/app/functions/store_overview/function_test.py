import configparser
import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
from datetime import date
import csv

# ----------------------------------------------------
# 建立 MySQL 連線
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

conn = mysql.connector.connect(**config)


now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")
# shopee events
# 讀取有活動參與的數據
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


df = pd.read_sql(event_sql, conn)
print(df)

target_date = pd.to_datetime("2023-05-17")
filtered_df = df.loc[df["date_time"] == target_date]

if not filtered_df.empty:
    result = filtered_df["product_page_views"].values[0]
    print(result)
else:
    print("No data found for the specified date.")

# 關閉資料庫連接
conn.close()