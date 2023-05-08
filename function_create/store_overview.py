# (V)1. 監控賣場經營分數(權重*當前數值，計算分數)
# 2. 高標 & 低標 highlight
# (V)3. 銷售額、商品瀏覽數、訪客數、成交量
# (V)4. 當日 highlight


import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

# 設定連線資訊
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

# 執行 SQL 「查看昨天是否有活動」

yday_event = "SELECT event FROM product_detail WHERE date_time = CURDATE()-1;"
step_times = "SELECT step_times FROM product_detail WHERE date_time = CURDATE()-1;"
new_visitors = "SELECT step_times FROM product_detail WHERE date_time = CURDATE()-1;"
return_visitors = "SELECT return_visitors FROM product_detail WHERE date_time = CURDATE()-1;"
product_page_views = "SELECT product_page_views FROM product_detail WHERE date_time = CURDATE()-1;"
search_clicks = "SELECT search_clicks FROM product_detail WHERE date_time = CURDATE()-1;"

def daily_data():
    yday_sales = "SELECT total_sales FROM product_detail WHERE date_time = CURDATE()-1;"
    return yday_sales
    step_times = "SELECT step_times FROM product_detail WHERE date_time = CURDATE()-1;"
    return step_times
    new_visitors = "SELECT step_times FROM product_detail WHERE date_time = CURDATE()-1;"
    return new_visitors
    return_visitors = "SELECT return_visitors FROM product_detail WHERE date_time = CURDATE()-1;"
    return return_visitors
    product_page_views = "SELECT product_page_views FROM product_detail WHERE date_time = CURDATE()-1;"
    return product_page_views
    search_clicks = "SELECT search_clicks FROM product_detail WHERE date_time = CURDATE()-1;"
    return search_clicks








def daily_report():
    if yday_event == 1:
        step_times = step_times / 82 * 56
        new_visitors = new_visitors / 221 * 20
        return_visitors = return_visitors / 187 * 17
        product_page_views = product_page_views / 2454 * 5
        search_clicks = search_clicks / 42 * 1

    else:
        step_times = step_times / 81 * 56
        new_visitors = new_visitors / 165 * 20
        return_visitors = return_visitors / 135 * 17
        product_page_views = product_page_views / 1841 * 5
        search_clicks = search_clicks / 36 * 1

    daily_report = step_times + new_visitors + return_visitors + product_page_views + search_clicks

    return daily_report

def daily_insight():
    if yday_event == 1:
        if step_times < 82:
            step_times = 82 - step_times
            return f"用戶停留時間低於平均{step_times}秒"
        if new_visitors < 221:
            new_visitors = 221 - new_visitors
            return f"新拜訪用戶低於平均{new_visitors}人"
        if return_visitors < 187:
            return_visitors = 187 - return_visitors
            return f"回訪用戶低於平均{return_visitors}人"
        if product_page_views < 2454:
            product_page_views = 2454 - product_page_views
            return f"商品頁面瀏覽數低於平均{product_page_views}次"
        if search_clicks < 42:
            search_clicks = 42 - search_clicks
            return f"搜尋點擊低於平均{search_clicks}次"

    else:
        if step_times < 81:
            step_times = 81 - step_times
            return f"用戶停留時間低於平均{step_times}秒"
        if new_visitors < 165:
            new_visitors = 165 - new_visitors
            return f"新拜訪用戶低於平均{new_visitors}人"
        if return_visitors < 135:
            return_visitors = 135 - return_visitors
            return f"回訪用戶低於平均{return_visitors}人"
        if product_page_views < 1841:
            product_page_views = 1841 - product_page_views
            return f"商品頁面瀏覽數低於平均{product_page_views}次"
        if search_clicks < 36:
            search_clicks = 36 - search_clicks
            return f"搜尋點擊低於平均{search_clicks}次"





# 


cursor.execute(query)

# 取得結果
result = cursor.fetchall()
print(result)
# 關閉 cursor 和連線
cursor.close()
cnx.close()

# ：
# 