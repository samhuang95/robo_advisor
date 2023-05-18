from flask import Flask, render_template, request, Blueprint
import pymysql
import datetime
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.offline as pyo
from functions.connect_to_db import SQLcommand

page_b = Blueprint('page_b', __name__)


# # 24種植物list
plant_list = ['銅鏡觀音蓮', '七變化虎耳草', '白斑姑婆芋', '明脈火鶴', '飄帶火鶴', '油畫竹芋', '巧克力皇后朱蕉',
              '斑葉豹紋竹芋', '大麻葉', '瑞士起司窗孔龜背芋', '大西瓜', '白斑龜背芋', '小西瓜', '紅玉椒草', '獨角獸',
              '灑金蔓綠絨', '白斑合果芋', '姬龜背芋', '黑頂卷柏', '斑葉白鶴芋', '黑合果芋', '台灣崖爬藤', '絨葉蔓綠絨',
              '斑葉心葉蔓綠絨']



def connect_mysql(plant_name, start_date, end_date):
    month_dict = dict()
    dates, sales = [], []
    sql = f"""
    SELECT * FROM robo_adviser.product_detail
    WHERE (product_name like '%{plant_name}%') AND (date_time BETWEEN '{start_date}' AND '{end_date}');
    """
    # cursor.execute(sql)
    # datas = cursor.fetchall()
    datas = SQLcommand.get(sql)
    for data in datas:
        # dates.append(data[0])
        # sales.append(data[14])
        if (str(data[0].year) + "年" + str(data[0].month) + "月") not in month_dict:
            month_dict[str(data[0].year) + "年" + str(data[0].month) + "月"] = data[14]
        else:
            month_dict[str(data[0].year) + "年" + str(data[0].month) + "月"] += data[14]
    for key, value in month_dict.items():
        dates.append(key)
        sales.append(value)
    return dates, sales


def month_list(start_datetime, end_datetime):
    start_date = start_datetime.date()
    end_date = end_datetime.date()
    start_date = start_date.replace(day=1)
    end_date = (end_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    current_date = start_date
    month1, month2 = [], []
    while current_date <= end_date:
        month1.append(current_date.strftime('%Y_%m'))
        month2.append(current_date.strftime('%Y年{}月').format(current_date.month))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    return month1, month2


def catch_predict(plant_name, start_date, end_date):
    month1, month2 = month_list(start_date, end_date)
    x, y = [], []
    for month in month1:
        try:
            sql = f"""
               SELECT * FROM robo_adviser.predict_total_sales_{month}
               """
            # cursor.execute(sql)
            # sales = cursor.fetchall()
            sales = SQLcommand.get(sql)
            print(sales)
            for item in sales:
                if item[0] == plant_name:
                    x.append(month2[month1.index(month)])
                    print(x)
                    y.append(int(item[1]))
        except:
            pass
    return x, y


# flask路由
@page_b.route('/b', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':  # 如果是 POST 請求
            start_date_str = request.form['start_date']  # 從 request.form 取得 start_date 參數
            end_date_str = request.form['end_date']  # 從 request.form 取得 end_date 參數
            plant_name = request.form['plant_name']
        else:  # 如果是 GET 請求
            start_date_str = request.args.get('start_date')  # 從 request.args 取得 start_date 參數
            end_date_str = request.args.get('end_date')  # 從 request.args 取得 end_date 參數
            plant_name = request.args.get('plant_name')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')  # 將 start_date_str 字串轉為 datetime 物件
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')  # 將 end_date_str 字串轉為 datetime 物件
        x, y = connect_mysql(plant_name, start_date, end_date)

        # delta = end_date - start_date   # 計算日期區間
        # every_date = [start_date + timedelta(days=i) for i in range(delta.days + 1)]   # 產生日期區間內每一天的日期
        fig = go.Figure()
        fig.add_trace(go.Bar(x=x, y=y, name='Group 1', text=y, textposition='auto', textangle=0, orientation='v'))
        fig.update_layout(barmode='group', title='Bar Chart')

        # fig = go.Figure()   # 建立一個 plotly 的 Figure 物件
        # fig.add_trace(go.Scatter(x=every_date, y=y, mode='lines+markers'))   # 在 Figure 物件中添加一個 Scatter 圖形
        # fig.update_layout(title=f'日期區間: {start_date_str} - {end_date_str}', xaxis_title='日期', yaxis_title='Value')   # 更新 Figure 物件的布
        #  # 将图表转换为HTML文件
        # div = opy.plot(fig, auto_open=False, output_type='div')
        # # 回傳 a頁面                         # 這個是圖像介面
        x2, y2 = catch_predict(plant_name, start_date, end_date)
        fig.add_trace(go.Bar(x=x2, y=y2, name='Group 2', text=y2, textposition='auto', textangle=0, orientation='v'))
        div = pyo.plot(fig, auto_open=False, output_type='div')
        return render_template("b.html", div_placeholder=div, plant_list=plant_list)
    except:
        return render_template("b.html", plant_list=plant_list)