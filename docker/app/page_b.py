from flask import render_template, request, Blueprint
import datetime
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.offline as pyo
from functions.connect_to_db import SQLcommand
from dateutil.relativedelta import relativedelta

page_b = Blueprint('page_b', __name__)

# # 24種植物list
plant_list = ['銅鏡觀音蓮', '七變化虎耳草', '白斑姑婆芋', '明脈火鶴', '飄帶火鶴', '油畫竹芋', '巧克力皇后朱蕉',
              '斑葉豹紋竹芋', '大麻葉', '瑞士起司窗孔龜背芋', '大西瓜', '白斑龜背芋', '小西瓜', '紅玉椒草', '獨角獸',
              '灑金蔓綠絨', '白斑合果芋', '姬龜背芋', '黑頂卷柏', '斑葉白鶴芋', '黑合果芋', '台灣崖爬藤', '絨葉蔓綠絨',
              '斑葉心葉蔓綠絨']


def connect_mysql(month):
    month_year = month[0:4]
    month_month = month.split("年")[1].replace("月", "")
    sales = []
    for plant in plant_list:
        sql = f"""
        SELECT total_sales FROM chi101.product_detail
        WHERE (product_name like '%{plant}%') AND 
        (YEAR(date_time) = {month_year} AND MONTH(date_time) = {month_month});
        """
        datas = SQLcommand().get(sql)
        sales_sum = 0
        for data in datas:
            sales_sum += data[0]
        sales.append(sales_sum)
    return sales


def list_year_month():
    start_year, start_month = 2021, 4
    end_year, end_month = datetime.now().year, (datetime.now() + relativedelta(months=1)).month
    month_list = []
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    current_date = start_date

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        month_list.append(f"{year}年{month}月")
        current_date += relativedelta(months=1)
    return month_list


def catch_predict(month):
    x, y = [], []
    new_month = month[0:4] + "_" + month.split("年")[1].replace("月", "").zfill(2)
    try:
        sql = f"""
           SELECT * FROM chi101.predict_total_sales_{new_month}
           """
        sales = SQLcommand().get(sql)
        for item in sales:
            x.append(item[0])
            y.append(int(item[1]))
    except:
        pass
    return x, y


# flask路由
@page_b.route('/b', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':  # 如果是 POST 請求
            month = request.form['month']
        else:  # 如果是 GET 請求
            month = request.args.get('month')
        x = plant_list
        y = connect_mysql(month)
        dict1 = {key: value for key, value in zip(x, y)}
        fig = go.Figure()
        fig.add_trace(go.Bar(x=y, y=x, name='月銷量', text=y, textposition='auto', textangle=0, orientation='h'))
        fig.update_layout(barmode='group', title='月銷量', xaxis_tickangle=45)
        x2, y2 = catch_predict(month)
        dict2 = {key: value for key, value in zip(x2, y2)}
        fig.add_trace(go.Bar(x=y2, y=x2, name='預測kpi', text=y2, textposition='auto', textangle=0, orientation='h'))
        div = pyo.plot(fig, auto_open=False, output_type='div')
        kpi = []
        if month != list_year_month()[-1]:
            for key in dict1:
                if key in dict2:
                    if dict1[key] < dict2[key]:
                        kpi.append(key + "：尚差" + str(dict2[key] - dict1[key]))
        return render_template("b.html", kpi=kpi, div_placeholder=div, month_list=list_year_month())
    except:
        return render_template("b.html", month_list=list_year_month())
