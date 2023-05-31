from flask import render_template, request, Blueprint
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import plotly.offline as pyo
from functions.connect_to_db import SQLcommand
from dateutil.relativedelta import relativedelta

page_b = Blueprint('page_b', __name__, url_prefix='/merchandising')

# 24種植物list
plant_list = ['銅鏡觀音蓮', '七變化虎耳草', '白斑姑婆芋', '明脈火鶴', '飄帶火鶴', '油畫竹芋', '巧克力皇后朱蕉',
              '斑葉豹紋竹芋', '大麻葉', '瑞士起司窗孔龜背芋', '大西瓜', '白斑龜背芋', '小西瓜', '紅玉椒草', '獨角獸',
              '灑金蔓綠絨', '白斑合果芋', '姬龜背芋', '黑頂卷柏', '斑葉白鶴芋', '黑合果芋', '台灣崖爬藤', '絨葉蔓綠絨',
              '斑葉心葉蔓綠絨']


# 連接mysql抓取全部商品，並對日銷量個別加總成月銷量
def connect_mysql_month(month):
    month_year = month[0:4]
    month_month = month.split("年")[1].replace("月", "")
    sales1 = []
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
        sales1.append(sales_num)
    return sales1


# 設定下拉式選單中的月份
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


# 抓取mysql中預測kpi的資料
def catch_predict(month):
    x, y = [], []
    new_month = month[0:4] + "_" + month.split("年")[1].replace("月", "").zfill(2)
    try:
        sql = f"""
            SELECT name, sales FROM chi101.predict_total_sales
            WHERE month = '{new_month}'
            """
        sales2 = SQLcommand().get(sql)
        for item in sales2:
            if item[1] > 0:
                x.append(int(item[1]))
            else:
                x.append(0)
            y.append(item[0])

    except:
        pass
    return x, y


def connect_mysql_plant(plant):
    sql = f"""
    SELECT date_time, total_sales FROM chi101.product_detail
    WHERE product_name LIKE '%{plant}%'
    """
    datas = SQLcommand().get(sql)
    sales_dict = {}
    for data in datas:
        year_month = data[0].strftime('%Y年%m月')
        if year_month in sales_dict:
            sales_dict[year_month] += data[1]
        else:
            sales_dict[year_month] = data[1]
    return list(sales_dict.values()), list(sales_dict.keys())


def catch_plant_predict(plant):
    sql = f"""
        SELECT month, sales FROM chi101.predict_total_sales
        WHERE name = '{plant}'
        """
    sales_dict = {}
    datas = SQLcommand().get(sql)
    for data in datas:
        year_month = data[0][0:4] + "年" + data[0][6].zfill(2) + "月"
        if data[1] >= 0:
            sales_dict[year_month] = int(data[1])
        else:
            sales_dict[year_month] = 0
    return list(sales_dict.values()), list(sales_dict.keys())


# flask路由
@page_b.route('/', methods=['GET', 'POST'])
def merchandising():
    try:
        # 獲取月份
        if request.method == 'POST':  # 如果是 POST 請求
            month = request.form['month']
        else:  # 如果是 GET 請求
            month = request.args.get('month')
        # 若無月分則設為當前月份
        if month is None:
            month = str(datetime.now().year) + "年" + str(datetime.now().month) + "月"

        # 繪製圖表
        fig = go.Figure()
        fig.update_layout(plot_bgcolor='#E9F4E8', barmode='group', title=dict(font=dict(size=25)), width=830,
                          height=800, xaxis_tickfont=dict(size=16), yaxis_tickfont=dict(size=16))
        x1 = connect_mysql_month(month)
        y1 = plant_list
        dict1 = {key: value for key, value in zip(y1, x1)}
        x2, y2 = catch_predict(month)
        dict2 = {key: value for key, value in zip(y2, x2)}
        temp_dict = {}
        # 表一為月銷量
        if month != list_year_month()[-1]:
            trace1 = go.Bar(x=x1, y=y1, text=[f"{num:,}" for num in x1], name='月銷量', textposition='auto', textangle=0, orientation='h',
                            marker=dict(color='#FF9933'))
            for key in dict1:
                if key in dict2:
                    if dict1[key] < dict2[key]:
                        temp_dict[key] = dict2[key] - dict1[key]
            fig.add_trace(trace1)

        # 表二為預測kpi
        if x2 != [] and y2 != []:
            trace2 = go.Bar(x=x2, y=y2, text=[f"{num:,}" for num in x2], name='預測kpi', textposition='auto', textangle=0, orientation='h',
                            marker=dict(color='#666666'))
            fig.add_trace(trace2)
            if month != list_year_month()[-1]:
                fig.update_layout(title=dict(font=dict(size=25)), height=1500)
            else:
                fig.update_layout(title=dict(font=dict(size=25)))
        fig.update_layout(yaxis=dict(autorange='reversed'))

        # 整理回傳kpi dict
        sorted_items = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
        kpi = [f"{key}: {value:,}" for key, value in sorted_items]
        
        # 回傳div給前端
        div = pyo.plot(fig, auto_open=False, output_type='div')
        return render_template("b.html", kpi=kpi, div_placeholder=div, month_list=list_year_month(),
                               selected_month=month)
    except:
        return render_template("b.html", month_list=list_year_month())


@page_b.route('/sales', methods=['GET', 'POST'])
def sales():
    try:
        # 獲取月份
        if request.method == 'POST':  # 如果是 POST 請求
            plant = request.form['plant']
        else:  # 如果是 GET 請求
            plant = request.args.get('plant')
        # 繪製圖表
        if plant:
            fig = go.Figure()
            fig.update_layout(plot_bgcolor='#E9F4E8', barmode='group', title=dict(font=dict(size=25)), width=830,
                              height=700, xaxis_tickfont=dict(size=16), yaxis_tickfont=dict(size=16))
            x1, y1 = connect_mysql_plant(plant)
            trace1 = go.Bar(x=x1, y=y1, text=[f"{num:,}" for num in x1], textfont=dict(size=16), name='月銷量', textposition='auto', textangle=0, orientation='h',
                            marker=dict(color='#FF9933'))
            fig.add_trace(trace1)
            x2, y2 = catch_plant_predict(plant)
            trace2 = go.Bar(x=x2, y=y2, text=[f"{num:,}" for num in x2], textfont=dict(size=16), name='預測kpi', textposition='auto', textangle=0, orientation='h',
                            marker=dict(color='#666666'))
            fig.add_trace(trace2)
            fig.update_layout(height=500+len(y1)*25)
            div = pyo.plot(fig, auto_open=False, output_type='div')
        return render_template("b_2.html", div_placeholder2=div, plant_list=plant_list, selected_plant=plant)
    except:
        return render_template("b_2.html", plant_list=plant_list)
