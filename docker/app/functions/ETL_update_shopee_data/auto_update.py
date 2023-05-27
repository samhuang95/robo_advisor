import datetime
import pandas as pd
import configparser
from datetime import date, datetime, timedelta
import numpy as np
import json
import csv

import sys
import os

# 取得上一層目錄的絕對路徑
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 將上一層目錄加入模組搜尋路徑
sys.path.append(parent_dir)
# import connect_to_db 模組
from connect_to_db import SQLcommand



# download data from shopee's background

now = datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

# update "product_overview"
# 讀取 xlsx 檔案
df = pd.read_excel(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv', index=False)
# 讀取 CSV 檔，並資料清洗

dtypes = {
    0: str, 1: int, 2: int, 3: int, 4: int,
    5: str, 6: int, 7: int, 8: int, 9: int,
    10: str, 11: int, 12: int, 13: int, 14: int,
    15: str, 16: int, 17: int, 18: int, 19: int,
    20: str, 21: str    
}
data = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100

# 【updata product_overview db】
mysql_column_names = '''(date_time, product_visitors, product_page_views, view_products, product_page_bounce_unique_visitors,
                product_page_bounce_rate, search_clicks, product_likes, `product_page_visitors(add_to_cart)`, 
                `add_to_cart(pcs)`, add_to_cart_conversion_rate, total_buyers, sale_products, 被購買的商品, total_sales, 
                sales_conversion_rate, `買家(可出貨訂單)`, `數量(可出貨訂單)`, 可出貨商品數量, `銷售額(可出貨訂單) (TWD)`, 
                `轉換率(可出貨訂單)`, 下單到可出貨轉換率)'''

csv_column_names = ['日期', '商品訪客數', '商品頁瀏覽數', '被瀏覽商品數', '跳出商品的不重複訪客',
                '商品頁的跳出率', '搜尋點擊', '商品按讚數', '商品頁訪客數(加入購物車)', 
                '加入購物車(件數)', '加入購物車轉換率', '買家(全部訂單)', '數量(全部訂單)', '被購買的商品', '銷售額(全部訂單) (TWD)', 
                '轉換率(全部訂單)', '買家(可出貨訂單)', '數量(可出貨訂單)', '可出貨商品數量', '銷售額(可出貨訂單) (TWD)', 
                '轉換率(可出貨訂單)', '下單到可出貨轉換率']

for i in range(len(data['日期'])):
    data_tuple = []
    for csv_column_name in csv_column_names:
        data_tuple.append(data[csv_column_name][i])
    # print(tuple(data_tuple))
    values_tuple = tuple(data_tuple)
    
    SQLcommand().modify(f'''
    INSERT IGNORE INTO product_overview 
        {mysql_column_names}
        VALUES {values_tuple}''')
    data_tuple = []

# ======================================================================================
# 【updata product_detail db】 
# 讀取 xlsx 檔案
df = pd.read_excel(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# ==============================================================
# 刪除不必要欄位
# 讀取 CSV 檔案
df = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', encoding='utf-8')
#刪除 2~5 欄
column_indices = [2, 3, 4, 5]

# 使用索引位置刪除欄位
df = df.drop(df.columns[column_indices], axis=1)

# 儲存更新後的內容到 CSV 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# ==============================================================
# 刪除沒有要使用的 row 
# 讀取 CSV 檔案
df = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', encoding='utf-8')
# 指定要刪除的標記
target_value = '-'
# 條件選擇 - 找出第二欄位值不為 '-' 的 row
mask = df.iloc[:, 2] != '-'
# 選擇符合條件的 row
df = df[mask]
# 儲存更新後的內容到 CSV 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# ==============================================================
# 新增時間欄位在第一格
# 開啟 CSV 檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', 'r', encoding='utf-8') as file:
    # 讀取 CSV 內容
    reader = csv.reader(file)
    rows = list(reader)

date_format = "%Y-%m-%d"
formatted_date = yesterday.strftime(date_format)
# 在每一列的第一欄位插入時間
for row in rows:
    row.insert(0, formatted_date)

# 寫入更新後的內容到 CSV 檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

dtypes = {
    0: str, 1: str, 2: str, 3: int, 4: int,
    5: int, 6: str, 7: int, 8: int, 9: int,
    10: int, 11: str, 12: int, 13: int, 14: int,
    15: str, 16: int, 17: int, 18: int, 19: str,
    20: str  
}
data = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100

mysql_column_names = '''(date_time, product_id, product_name, product_visitors, product_page_views,
                product_page_bounce_unique_visitors, product_page_bounce_rate, search_clicks, product_likes, `product_page_visitors(add_to_cart)`, 
                `add_to_cart(pcs)`, add_to_cart_conversion_rate, total_buyers, sale_products, total_sales, 
                sales_conversion_rate, `買家(可出貨訂單)`, `數量(可出貨訂單)`, `銷售額(可出貨訂單) (TWD)`, `轉換率(可出貨訂單)`, 
                全部訂單到可出貨訂單的轉換率)'''

csv_column_names = [f'{year}-{month}-{day}','商品ID', '商品名稱', '商品訪客數', '商品訪客數', '跳出商品的不重複訪客',
                 '商品頁的跳出率', '搜尋點擊', '商品按讚數', '商品頁訪客數(加入購物車)', 
                 '加入購物車(件數)', '加入購物車轉換率', '買家(全部訂單)', '數量(全部訂單)', '銷售額(全部訂單) (TWD)', '轉換率(全部訂單)', 
                 '買家(可出貨訂單)', '數量(可出貨訂單)', '銷售額(可出貨訂單) (TWD)', '轉換率(可出貨訂單)', '全部訂單到可出貨訂單的轉換率']

for i in range(len(data['商品ID'])):
    data_tuple = []
    for csv_column_name in csv_column_names:
        data_tuple.append(data[csv_column_name][i])
    values_tuple = tuple(data_tuple)
    
    SQLcommand().modify(f'''
    INSERT IGNORE INTO product_detail 
        {mysql_column_names}
        VALUES {values_tuple}''')
    data_tuple = []

# ======================================================================
# 【updata traffic_overview db】 
# 讀取 xlsx 檔案
df = pd.read_excel(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# =====================================
# 刪除不必要欄位
# 讀取 CSV 前兩行檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [next(reader) for _ in range(2)]  # 讀取前兩行資料，包括標題行
    
    date_format = "%Y-%m-%d"
    formatted_date = yesterday.strftime(date_format)
    
    data = [[formatted_date] + [row[i] for i in range(len(row)) if i != 0] for row in data]  # 插入日期作為第一個欄位
# 寫入輸出的 CSV 檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)   # 寫入前兩行資料

dtypes = {
    0: str, 1: int, 2: float, 3: str, 4: str,
    5: int, 6: int, 7: int, 8: int
}
data = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100

mysql_column_names = '''(date_time, page_views, avg_page_views, time_on_page, bounce_rate,
                 unique_visitors, new_visitors, return_visitors, new_fans)'''

csv_column_names = [f'{year}-{month}-{day}', '頁面瀏覽數', '頁面平均瀏覽次數', '頁面平均停留時間', '頁面跳出率', '不重複訪客數', 
                    '不重複訪客數', '既有的訪客數', '新的粉絲數']

for i in range(len(data['頁面瀏覽數'])):
    data_tuple = []
    for csv_column_name in csv_column_names:
        data_tuple.append(data[csv_column_name][i])
    values_tuple = tuple(data_tuple)
    
    SQLcommand().modify(f'''
    INSERT IGNORE INTO traffic_overview 
        {mysql_column_names}
        VALUES {values_tuple}''')
    data_tuple = []

# ======================================================================
# ======================================================================
# # 【updata stats db】 
# 讀取 xlsx 檔案
df = pd.read_excel(f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.xlsx')
# 寫入 csv 檔案
df.to_csv(f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', index=False, encoding='utf-8')
# 讀取 CSV 檔，並資料清洗
# =====================================
# 刪除不必要欄位
# 讀取 CSV 前兩行檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [next(reader) for _ in range(2)]  # 讀取前兩行資料，包括標題行
    
    date_format = "%Y-%m-%d"
    formatted_date = yesterday.strftime(date_format)
    
    data = [[formatted_date] + [row[i] for i in range(len(row)) if i != 0] for row in data]  # 插入日期作為第一個欄位
# 寫入輸出的 CSV 檔案
with open(f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)   # 寫入前兩行資料

dtypes = {
    0: str, 1: int, 2: int, 3: float, 4: int,
    5: int, 6: str, 7: int, 8: int, 9: int, 
    10: int, 11: int, 12: int, 13: int, 14: int, 15: str
}
data = pd.read_csv(f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv', thousands=',', dtype=dtypes, encoding='utf-8')
# 將百分比轉換成小數
for col in data.columns:
    if data[col].dtype == 'object' and '%' in data[col].iloc[0]:
        data[col] = data[col].str.rstrip('%').astype('float') / 100

mysql_column_names = '''(date_time, total_sales, total_orders, avg_order_values, page_views,
                  visitors, paid_conversion_rate, invalid_order, invalid_order_values, return_orders, 
                  return_order_values, buyers, new_buyers, return_buyers, prospect_buyers, 
                  repurchase_rate)'''

csv_column_names = [f'{year}-{month}-{day}', '總銷售額 (TWD)', '訂單總數', '平均訂單金額', '頁面瀏覽數', '訪客數', 
                    '付款轉換率', '不成立的訂單', '不成立訂單的銷售額', '退貨/退款訂單', '退貨/退款的銷售額', '買家數', '新買家數', 
                    '舊買家數', '潛在買家數', '回購率']

for i in range(len(data['訂單總數'])):
    data_tuple = []
    for csv_column_name in csv_column_names:
        data_tuple.append(data[csv_column_name][i])
    values_tuple = tuple(data_tuple)
    
    SQLcommand().modify(f'''
    INSERT IGNORE INTO stats 
        {mysql_column_names}
        VALUES {values_tuple}''')
    data_tuple = []


# 刪除所有暫存的下載類資料

# 指定要刪除的檔案路徑
file_path1 = f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.csv'
file_path2 = f'/app/functions/ETL_update_shopee_data/csv_download/flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.xlsx'
file_path3 = f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.csv'
file_path4 = f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.xlsx'
file_path5 = f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.csv'
file_path6 = f'/app/functions/ETL_update_shopee_data/csv_download/export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.xlsx'
file_path7 = f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.csv'
file_path8 = f'/app/functions/ETL_update_shopee_data/csv_download/[export_report]productoverview{year}{month}{day}-{year}{month}{day}.xlsx'

# 刪除檔案
file_paths = [file_path1, file_path2, file_path3, file_path4, file_path5, file_path6, file_path7, file_path8]

for file_path in file_paths:
    os.remove(file_path)