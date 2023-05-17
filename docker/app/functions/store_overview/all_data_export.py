from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import csv
from datetime import date, datetime, timedelta
import mysql.connector
import configparser


now = datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

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


# 獨立匯出一包不分活動與否的 all_data
event_sql = '''
SELECT 
    date_time AS 'date', 
    SUM(total_sales) AS 'daily_sales'
FROM 
    tibame_project.product_detail
GROUP BY 
    date_time;'''
result = pd.read_sql(event_sql, cnx)

# 將結果轉成 DataFrame，並儲存下來
df = pd.DataFrame(result)
now = datetime.now()
yesterday = (now - timedelta(days=1)).date()
df.to_csv(f'./dataset/all_data{yesterday}.csv', index=False)


# 新增店家名稱在第一格
# 開啟 CSV 檔案
df = pd.read_csv(f'./dataset/all_data{yesterday}.csv')

# 在第二欄新增一個名為 "New_Column" 的欄位，並將所有值設置為 "宅栽工作室"
df.insert(1, "shop_name", "宅栽工作室")

# 儲存修改後的結果回到 CSV 檔案
df.to_csv(f'./dataset/all_data{yesterday}.csv', index=False)


# 關閉 cursor 和連線
cursor.close()
cnx.close()