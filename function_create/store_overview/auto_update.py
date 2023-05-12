import pandas as pd
import configparser
import mysql.connector

# download data from shopee's background


























# 讀取 CSV 檔案
data = pd.read_csv(f'export_report.parentskudetail.{today()}_{}.csv')
# export_report.parentskudetail.20210430_20210430
# 設定連線資訊
config = configparser.ConfigParser()
config.read('config.ini')

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
table_name = 'product_detail'
columns = ','.join(data.columns)
values = ','.join(['%s'] * len(data.columns))
query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

# 匯入資料
for row in data.itertuples(index=False):
    cursor.execute(query, tuple(row))

# 提交變更
cnx.commit()

# 關閉 cursor 和連線
cursor.close()
cnx.close()
