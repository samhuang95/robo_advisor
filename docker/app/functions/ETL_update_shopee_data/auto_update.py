import datetime
import pandas as pd
import configparser
import mysql.connector
from datetime import date, datetime, timedelta
import numpy as np
# download data from shopee's background




# update "product_overview"
# 讀取 CSV 檔案
now = datetime.now().date()
yesterday = now - timedelta(days=1)


year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")




import pandas as pd


# 讀取 xlsx 檔案
df = pd.read_excel(f'./csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.xlsx')


# 寫入 csv 檔案
df.to_csv(f'./csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv', index=False)


# 讀取 CSV 檔 資料清洗


dtypes = {
    0: str, 1: int, 2: int, 3: int, 4: int,
    5: str, 6: int, 7: int, 8: int, 9: int,
    10: str, 11: int, 12: int, 13: int, 14: int,
    15: str, 16: int, 17: int, 18: int, 19: int,
    20: str, 21: str    
}
data = pd.read_csv(f'./csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100










# 設定連線資訊
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


config = {
    'user': config.get('store_overview', 'user'),
    'password': config.get('store_overview', 'password'),
    'host': config.get('store_overview', 'host'),
    'database': config.get('store_overview', 'database'),
    'port': config.get('store_overview', 'port'),
    # 'use_pure':config.get('store_overview', 'use_pure')
}


# 建立連線
cnx = mysql.connector.connect(**config)


# 建立 cursor
cursor = cnx.cursor()


# 建立 SQL 語句
table_name = 'tibame_project.product_overview'
columns = ','.join(data.columns)
values = ','.join(['%s'] * len(data.columns))


# 將 DataFrame 轉換成 records array 的形式
data = data.where(pd.notnull(data), None)
# 將 DataFrame 轉換成 records array 的形式
data = data.where(pd.notnull(data), None)
data = data.applymap(lambda x: int(x) if np.issubdtype(type(x), np.integer) else x)
data = data.applymap(lambda x: float(x) if np.issubdtype(type(x), np.floating) else x)


records = data.to_records(index=False)


query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"


# 匯入資料
for record in records:
    # 處理百分比轉換成小數
    row = [float(val.rstrip('%')) / 100 if isinstance(val, str) and '%' in val else val for val in record]
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", tuple(row))


# records = data.to_records(index=False)


# query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"


# 匯入資料
# for record in records:
#     # 處理百分比轉換成小數
#     row = [float(val.rstrip('%')) / 100 if isinstance(val, str) and '%' in val else val for val in record]
#     cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", row)


# 提交變更
cnx.commit()


# 關閉 cursor 和連線
cursor.close()
cnx.close()