import csv
from datetime import date
today = date.today()
# 讀取沒有活動的權重
with open(f'./dataset/noevent_weight{today}.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    weight_dict = {}
    for event_weight in reader:
    # 將每一筆資料轉換成 dictionary
        feature = event_weight['feature']
        importance = event_weight['importance']
        weight_dict[feature] = importance
    # 獲取資料變數
    noevent_product_page_views = float(weight_dict['product_page_views'])
    noevent_step_times = float(weight_dict['step_times'])
    noevent_product_page_bounce_rate = float(weight_dict['product_page_bounce_rate'])
    noevent_unique_visitors = float(weight_dict['unique_visitors'])
    noevent_new_visitors = float(weight_dict['new_visitors'])
    noevent_return_visitors = float(weight_dict['return_visitors'])
    noevent_new_fans = float(weight_dict['new_fans'])
    noevent_search_clicks = float(weight_dict['search_clicks'])
    noevent_product_likes = float(weight_dict['product_likes'])
    

    noevent_SUM = noevent_product_page_views + noevent_step_times + noevent_product_page_bounce_rate + noevent_unique_visitors + noevent_new_visitors + noevent_return_visitors + noevent_new_fans + noevent_search_clicks + noevent_product_likes
    
    prop_noevent_product_page_views = noevent_product_page_views / noevent_SUM * 100
    prop_noevent_step_times = noevent_step_times / noevent_SUM * 100
    prop_noevent_product_page_bounce_rate = noevent_product_page_bounce_rate / noevent_SUM * 100
    prop_noevent_unique_visitors = noevent_unique_visitors / noevent_SUM * 100
    prop_noevent_new_visitors = noevent_new_visitors / noevent_SUM * 100
    prop_noevent_return_visitors = noevent_return_visitors / noevent_SUM * 100
    prop_noevent_new_fans = noevent_new_fans / noevent_SUM * 100
    prop_noevent_search_clicks = noevent_search_clicks / noevent_SUM * 100
    prop_noevent_product_likes = noevent_product_likes / noevent_SUM * 100
    