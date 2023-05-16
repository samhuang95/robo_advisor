import datetime
import pandas as pd
import configparser
import mysql.connector
from datetime import date, datetime, timedelta
import numpy as np
import json
import csv
# download data from shopee's background


now = datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

# update "product_overview"
# 讀取 xlsx 檔案
df = pd.read_excel(f'./csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'./csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv', index=False)
# 讀取 CSV 檔，並資料清洗

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
    'database': config.get('store_overview', 'database')
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
data = data.applymap(lambda x: int(x) if isinstance(x, np.int64) else x)
data = data.applymap(lambda x: float(x) if isinstance(x, np.float64) else x)

# print(data)

records = data.to_records(index=False)

for row_nums in range(len(records)):
    JSON = {}
    for colunm_num in range(len(records[0])):
        value = records[row_nums][colunm_num]
        if type(value) == str:
            # 將字串轉換為 datetime 物件
            datetime_obj = datetime.strptime(value, '%Y-%m-%d %H:%M')
            # 將 datetime 物件轉換為 MySQL DATETIME 格式
            mysql_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:00')
            JSON[colunm_num] = mysql_datetime

        if type(value) == np.int64:
            JSON[colunm_num] = int(value)

        if type(value) == np.float64:
            JSON[colunm_num] = float(value)

    # 建立 SQL 語句
    table_name = '`tibame_project`.`product_overview`'
    columns = ','.join([f'`{index}`' for index in range(len(JSON))])
    values = ','.join(['%s'] * len(JSON))
    query = f"INSERT INTO {table_name} VALUES ({values})"

    # 執行插入操作
    cursor.execute(query, tuple(JSON.values()))

    # 提交變更
    cnx.commit()
    JSON = {}

# ======================================================================
# ======================================================================
# update "product_detail"
# 讀取 xlsx 檔案
df = pd.read_excel(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# ==============================================================
# 刪除不必要欄位
# 讀取 CSV 檔案
df = pd.read_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', encoding='utf-8')
#刪除 2~5 欄
column_indices = [2, 3, 4, 5]

# 使用索引位置刪除欄位
df = df.drop(df.columns[column_indices], axis=1)

# 儲存更新後的內容到 CSV 檔案
df.to_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# ==============================================================
# 刪除沒有要使用的 row 
# 讀取 CSV 檔案
df = pd.read_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', encoding='utf-8')
# 指定要刪除的標記
target_value = '-'
# 條件選擇 - 找出第二欄位值不為 '-' 的 row
mask = df.iloc[:, 2] != '-'
# 選擇符合條件的 row
df = df[mask]
# 儲存更新後的內容到 CSV 檔案
df.to_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# ==============================================================
# 新增時間欄位在第一格
# 開啟 CSV 檔案
with open(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', 'r', encoding='utf-8') as file:
    # 讀取 CSV 內容
    reader = csv.reader(file)
    rows = list(reader)

date_format = "%Y-%m-%d"
formatted_date = yesterday.strftime(date_format)
# 在每一列的第一欄位插入時間
for row in rows:
    row.insert(0, formatted_date)

# 寫入更新後的內容到 CSV 檔案
with open(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

dtypes = {
    0: str, 1: str, 2: str, 3: int, 4: int,
    5: int, 6: str, 7: int, 8: int, 9: int,
    10: int, 11: str, 12: int, 13: int, 14: int,
    15: str, 16: int, 17: int, 18: int, 19: str,
    20: str  
}
data = pd.read_csv(f'./csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
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
    'database': config.get('store_overview', 'database')
}

# 建立連線
cnx = mysql.connector.connect(**config)

# 建立 cursor
cursor = cnx.cursor()

# 建立 SQL 語句
table_name = 'tibame_project.product_detail'
columns = ','.join(data.columns)
values = ','.join(['%s'] * len(data.columns))

# 將 DataFrame 轉換成 records array 的形式
data = data.where(pd.notnull(data), None)
data = data.applymap(lambda x: int(x) if isinstance(x, np.int64) else x)
data = data.applymap(lambda x: float(x) if isinstance(x, np.float64) else x)

# print(data)

records = data.to_records(index=False)

for row_nums in range(len(records)):
    JSON = {}
    for colunm_num in range(len(records[0])):
        value = records[row_nums][colunm_num]
        if colunm_num == 0:
            # 將字串轉換為 datetime 物件
            datetime_obj = datetime.strptime(value, '%Y-%m-%d')
            # 將 datetime 物件轉換為 MySQL DATETIME 格式
            mysql_datetime = datetime_obj.strftime('%Y-%m-%d')
            JSON[colunm_num] = mysql_datetime

        if colunm_num == 1:  # 第一欄為商品ID，轉換為VARCHAR(20)
            JSON[colunm_num] = str(value)

        if colunm_num == 2:  # 第12欄為商品名稱，轉換為TEXT
            JSON[colunm_num] = str(value)

        if type(value) == np.int64:
            JSON[colunm_num] = int(value)

        if type(value) == np.float64:
            JSON[colunm_num] = float(value)

    # 建立 SQL 語句
    table_name = '`tibame_project`.`product_detail`'
    columns = ','.join([f'`{index}`' for index in range(len(JSON))])
    values = ','.join(['%s'] * len(JSON))
    query = f"INSERT INTO {table_name} VALUES ({values})"

    # 執行插入操作
    cursor.execute(query, tuple(JSON.values()))

    # 提交變更
    cnx.commit()
    JSON = {}

# ======================================================================
# ======================================================================
# update "traffic_overview"
# 讀取 xlsx 檔案
df = pd.read_excel(f'./csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'./csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# =====================================
# 刪除不必要欄位
# 讀取 CSV 前兩行檔案
with open(f'./csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [next(reader) for _ in range(2)]  # 讀取前兩行資料，包括標題行
    
    date_format = "%Y-%m-%d"
    formatted_date = yesterday.strftime(date_format)
    
    data = [[formatted_date] + [row[i] for i in range(len(row)) if i != 0] for row in data]  # 插入日期作為第一個欄位
# 寫入輸出的 CSV 檔案
with open(f'./csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)   # 寫入前兩行資料

dtypes = {
    0: str, 1: int, 2: float, 3: str, 4: str,
    5: int, 6: int, 7: int, 8: int
}
data = pd.read_csv(f'./csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100


# =====================================
# 設定連線資訊
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

config = {
    'user': config.get('store_overview', 'user'),
    'password': config.get('store_overview', 'password'),
    'host': config.get('store_overview', 'host'),
    'database': config.get('store_overview', 'database')
}

# 建立連線
cnx = mysql.connector.connect(**config)

# 建立 cursor
cursor = cnx.cursor()

# 建立 SQL 語句
table_name = 'tibame_project.traffic_overview'
columns = ','.join(data.columns)
values = ','.join(['%s'] * len(data.columns))

# 將 DataFrame 轉換成 records array 的形式
# data = data.where(pd.notnull(data), None)
data = data.fillna(value=pd.NA)
data = data.applymap(lambda x: int(x) if isinstance(x, np.int64) else x)
data = data.applymap(lambda x: float(x) if isinstance(x, np.float64) else x)
print(data)

records = data.to_records(index=False)
print('===============')
print(type(records[0][0]))
for row_nums in range(len(records)):
    JSON = {}
    for colunm_num in range(len(records[0])):
        value = records[row_nums][colunm_num]
        if colunm_num == 0:
            # 將字串轉換為 datetime 物件
            datetime_obj = datetime.strptime(value, '%Y-%m-%d')
            # 將 datetime 物件轉換為 MySQL DATETIME 格式
            mysql_datetime = datetime_obj.strftime('%Y-%m-%d')
            JSON[colunm_num] = mysql_datetime

        elif colunm_num == 3:
            # 將字串轉換為 datetime 物件
            datetime_obj = datetime.strptime(value, '%H:%M:%S')
            # 將 datetime 物件轉換為 MySQL DATETIME 格式
            mysql_datetime = datetime_obj.strftime('%H:%M:%S')
            JSON[colunm_num] = mysql_datetime

        elif type(value) == np.int64:
            JSON[colunm_num] = int(value)

        elif type(value) == np.float64:
            JSON[colunm_num] = float(value)
        else:
            JSON[colunm_num] = value  # 不是 int 或 float 的值，直接賦值
    print(JSON)
    # 建立 SQL 語句
    table_name = '`tibame_project`.`traffic_overview`'
    columns = ','.join([f'`{index}`' for index in range(len(JSON))])
    values = ','.join(['%s'] * len(JSON))
    query = f"INSERT INTO {table_name} VALUES ({values})"

    # 執行插入操作
    cursor.execute(query, tuple(JSON.values()))

    # 提交變更
    cnx.commit()
    
    JSON = {}


# ======================================================================
# ======================================================================
# update "stats"
# 讀取 xlsx 檔案
df = pd.read_excel(f'./csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'./csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# =====================================
# 刪除不必要欄位
# 讀取 CSV 前兩行檔案
with open(f'./csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [next(reader) for _ in range(2)]  # 讀取前兩行資料，包括標題行
    
    date_format = "%Y-%m-%d"
    formatted_date = yesterday.strftime(date_format)
    
    data = [[formatted_date] + [row[i] for i in range(len(row)) if i != 0] for row in data]  # 插入日期作為第一個欄位
# 寫入輸出的 CSV 檔案
with open(f'./csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)   # 寫入前兩行資料

dtypes = {
    0: str, 1: int, 2: int, 3: float, 4: int,
    5: int, 6: str, 7: int, 8: int, 9: int, 
    10: int, 11: int, 12: int, 13: int, 14: int, 15: str
}
data = pd.read_csv(f'./csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100


# =====================================
# 設定連線資訊
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

config = {
    'user': config.get('store_overview', 'user'),
    'password': config.get('store_overview', 'password'),
    'host': config.get('store_overview', 'host'),
    'database': config.get('store_overview', 'database')
}

# 建立連線
cnx = mysql.connector.connect(**config)

# 建立 cursor
cursor = cnx.cursor()

# 建立 SQL 語句
table_name = 'tibame_project.stats'
columns = ','.join(data.columns)
values = ','.join(['%s'] * len(data.columns))

# 將 DataFrame 轉換成 records array 的形式
# data = data.where(pd.notnull(data), None)
data = data.fillna(value=pd.NA)
data = data.applymap(lambda x: int(x) if isinstance(x, np.int64) else x)
data = data.applymap(lambda x: float(x) if isinstance(x, np.float64) else x)
print(data)

records = data.to_records(index=False)
print('===============')
print(type(records[0][0]))
for row_nums in range(len(records)):
    JSON = {}
    for colunm_num in range(len(records[0])):
        value = records[row_nums][colunm_num]
        if colunm_num == 0:
            # 將字串轉換為 datetime 物件
            datetime_obj = datetime.strptime(value, '%Y-%m-%d')
            # 將 datetime 物件轉換為 MySQL DATETIME 格式
            mysql_datetime = datetime_obj.strftime('%Y-%m-%d')
            JSON[colunm_num] = mysql_datetime

        elif type(value) == np.int64:
            JSON[colunm_num] = int(value)

        elif type(value) == np.float64:
            JSON[colunm_num] = float(value)
        # else:
        #     JSON[colunm_num] = value  # 不是 int 或 float 的值，直接賦值
    print(JSON)
    # 建立 SQL 語句
    table_name = '`tibame_project`.`stats`'
    columns = ','.join([f'`{index}`' for index in range(len(JSON))])
    values = ','.join(['%s'] * len(JSON))
    query = f"INSERT INTO {table_name} VALUES ({values})"

    # 執行插入操作
    cursor.execute(query, tuple(JSON.values()))

    # 提交變更
    cnx.commit()
    
    JSON = {}
# 關閉 cursor 和連線
cursor.close()
cnx.close()