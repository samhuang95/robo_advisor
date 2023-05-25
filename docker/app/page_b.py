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
    plant_string = " or ".join(["product_name like'%" + plant + "%'" for plant in plant_list])
    sql = f"""
    SELECT product_name, total_sales FROM chi101.product_detail
    WHERE ({plant_string}) AND 
    (YEAR(date_time) = {month_year} AND MONTH(date_time) = {month_month});
    """
    datas = SQLcommand().get(sql)
    for plant in plant_list:
        sales_num = 0
        for data in datas:
            if data[0].find(plant) != -1:
                sales_num += data[1]
        sales.append(sales_num)
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
            if item[1] > 0:
                x.append(int(item[1]))
            else:
                x.append(0)
            y.append(item[0])

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
        x1 = connect_mysql(month)
        y1 = plant_list
        dict1 = {key: value for key, value in zip(y1, x1)}
        fig = go.Figure()
        fig.update_layout(barmode='group', title=dict(text='月銷量', font=dict(size=25)), width=830, height=800, xaxis_tickfont=dict(size=16), yaxis_tickfont=dict(size=16))
        x2, y2 = catch_predict(month)
        dict2 = {key: value for key, value in zip(y2, x2)}
        kpi = []
        if x2 != [] and y2 != []:
            trace2 = go.Bar(x=x2, y=y2, name='預測kpi', textposition='auto', textangle=0, orientation='h', marker=dict(color='red'))
            text2_labels = [str(x) if x != 0 else '0' for x in x2]
            trace2.text = text2_labels
            fig.add_trace(trace2)
            if month != list_year_month()[-1]:
                fig.update_layout(title=dict(text='月銷量+預測kpi', font=dict(size=25)), height=1500)
                # for i, x in enumerate(x2):
                #     if x == 0:
                #         fig.add_annotation(y=y2[i], x=x, text=str(x), showarrow=False, xshift=5, yshift=-10)
            else:
                fig.update_layout(title=dict(text='預測kpi', font=dict(size=25)))
                # for i, x in enumerate(x2):
                #     if x == 0:
                #         fig.add_annotation(y=y2[i], x=x, text=str(x), showarrow=False, xshift=5)

        if month != list_year_month()[-1]:
            trace1 = go.Bar(x=x1, y=y1, name='月銷量', textposition='auto', textangle=0, orientation='h', marker=dict(color='blue'))
            text1_labels = [str(x) if x != 0 else '0' for x in x1]
            trace1.text = text1_labels
            fig.add_trace(trace1)
            for key in dict1:
                if key in dict2:
                    if dict1[key] < dict2[key]:
                        kpi.append(f"""{key}：{dict2[key] - dict1[key]}""")
            # if x2 == [] and y2 == []:
            #     for i, x in enumerate(x1):
            #         if x == 0:
            #             fig.add_annotation(y=y1[i], x=x, text=str(x), showarrow=False, xshift=5)
            # else:
            #     for i, x in enumerate(x1):
            #         if x == 0:
            #             fig.add_annotation(y=y1[i], x=x, text=str(x), showarrow=False, xshift=5, yshift=10)


        div = pyo.plot(fig, auto_open=False, output_type='div')
        return render_template("b.html", kpi=kpi, div_placeholder=div, month_list=list_year_month(), selected_month=month)
    except:
        return render_template("b.html", month_list=list_year_month())

