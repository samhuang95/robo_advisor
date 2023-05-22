from pyecharts.charts import Line
from pyecharts import options as opts
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from flask import Flask, render_template
import sys
sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from connect_to_db import SQLcommand


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
GROUP BY 
    pd.date_time, t.date_time
HAVING 
    MONTH(t.date_time) = DAY(t.date_time) OR 
    DAY(t.date_time) = 18 OR
    (DAYOFWEEK(t.date_time) = 4)
ORDER BY 1 DESC;
    ''')

# print(len(df))
df = pd.DataFrame(df)
print(df[1].mean())