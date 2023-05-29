from plants_forecating_model import predict_column
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import schedule
from functions.connect_to_db import SQLcommand


# 閏年判斷
def is_leap_year(year: int):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


# 月份天數判斷
def month_date(m: int) -> int:
    now_time = datetime.now()
    month1 = [1, 3, 5, 7, 8, 10, 12]
    if m in month1:
        return 31
    elif m == 2:
        if is_leap_year(now_time.year):
            return 29
        return 28
    else:
        return 30


# 植物清單
plant_list = ['銅鏡觀音蓮', '七變化虎耳草', '白斑姑婆芋', '明脈火鶴', '飄帶火鶴', '油畫竹芋', '巧克力皇后朱蕉',
              '斑葉豹紋竹芋', '大麻葉', '瑞士起司窗孔龜背芋', '大西瓜', '白斑龜背芋', '小西瓜', '紅玉椒草', '獨角獸',
              '灑金蔓綠絨', '白斑合果芋', '姬龜背芋', '黑頂卷柏', '斑葉白鶴芋', '黑合果芋', '台灣崖爬藤', '絨葉蔓綠絨',
              '斑葉心葉蔓綠絨']


# 執行預測
def start_predict(year_month):
    year = int(year_month[:4])
    month = int(year_month[-2:])
    orig_dict_date = dict()
    orig_dict_month = dict()
    pred_dict = dict()
    try:
        # 建立預測資料的資料庫
        sql1 = f"""
            CREATE TABLE predict_total_sales_{year}_{str(month).zfill(2)} (NAME text, sales float);
            """
        SQLcommand().modify(sql1)
    except:
        print('db already exists')


    # 對每種植物進行資料庫讀取並放入orig_dict_date中
    for n in plant_list:
        sql2 = f"""
            SELECT date_time, total_sales FROM chi101.product_detail
            WHERE product_name like '%{n}%' AND (date_time < '{year_month}-15');
            """
        datas = SQLcommand().get(sql2)
        for data in datas:
            if n not in orig_dict_date.keys():
                orig_dict_date[n] = [[data[0], data[1]]]
            else:
                orig_dict_date[n].append([data[0], data[1]])

    # 將每月數量加總並放入orig_dict_month中
    for key, values in orig_dict_date.items():
        # print(key)
        for value in values:
            if key not in orig_dict_month:
                orig_dict_month[key] = {str(value[0])[2:7]: value[1]}
            else:
                if str(value[0])[2:7] not in orig_dict_month[key]:
                    orig_dict_month[key][str(value[0])[2:7]] = value[1]
                else:
                    orig_dict_month[key][str(value[0])[2:7]] += value[1]

    # 呼叫預測程式，並將預測結果匯入資料庫
    sum_avg = {}
    for key, values in orig_dict_month.items():
        item_list = [item[1] for item in orig_dict_date[key]]
        x = pd.Series(item_list)
        if month != 12:
            predictions_df = predict_column(x, (month_date(month) + month_date(month + 1) - 15))
        else:
            predictions_df = predict_column(x, (month_date(month) + 31 - 15))
        pred = sum([item[0] for item in predictions_df.values.tolist()][month_date(month):])
        if key not in pred_dict.keys():
            pred_dict[key] = {year_month: pred}
        else:
            pred_dict[key][year_month] = pred

        if key not in sum_avg.keys():
            sum_avg[key] = {year_month: month_date((datetime.now() + relativedelta(months=1)).month)*sum(item_list)/(len(item_list)-(month_date(month)))}
        else:
            sum_avg[key][year_month] = month_date((datetime.now() + relativedelta(months=1)).month)*sum(item_list)/(len(item_list)-(month_date(month)))
        print(sum_avg)
        print(pred_dict)
        sql3 = f"""
            INSERT INTO predict_total_sales_{year}_{str(month).zfill(2)} (NAME, SALES)
            VALUES ('{key}', {pred});
            """
        SQLcommand().modify(sql3)


# 每個月15號執行plant_kpi
def job():
    today = datetime.date.today()
    new = today + relativedelta(months=1)
    new_month = str(new.year) + str(new.month).zfill(2)
    if today.day == 15:
        start_predict(new_month)
        print("執行程式 - 15號")


schedule.every().day.at("00:00").do(job)
while True:
    schedule.run_pending()