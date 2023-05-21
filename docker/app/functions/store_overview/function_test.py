import sys
sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from connect_to_db import SQLcommand

df = SQLcommand().get('''
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
    traffic_overview t
        JOIN product_detail pd
            ON t.date_time = pd.date_time
GROUP BY 
    pd.date_time, t.date_time
ORDER BY 1 DESC
LIMIT 1;
    ''')

print(df[0][0])