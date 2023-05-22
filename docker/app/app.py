from datetime import datetime, timedelta
from flask import Flask, render_template, request
from functions.store_overview.adj_store_overview import *
# from functions.store_overview.goal import line_stack_area
from functions.connect_to_db import SQLcommand
from functions.image_predict import predict_image
from functions.clear_folder import clear_folder
from BCG_funtions import *
import random
import logging
import plotly.graph_objs as go 
import plotly.offline as opy


# ==============德柔功能
from competitor_draw_chart import DrawChart
from datetime import datetime


app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)



# 做一個註冊的路由
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    user_name = request.form['user_name']
    user_password = request.form['user_password']

    data = SQLcommand().get(f'SELECT * FROM user_data WHERE account = "{user_name}"')
    if data: return '此帳號已經有人使用'
    
    SQLcommand().modify(f'INSERT INTO user_data (account, password) VALUES ("{user_name}", "{user_password}")')

    return render_template("signin.html")


# 做一個登入的路由
@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")

    user_name = request.form['user_name']
    user_password = request.form['user_password']

    data = SQLcommand().get(f'SELECT * FROM user_data WHERE account = "{user_name}"')
    if not data:
        return render_template("signin.html", warning='請註冊帳號')
    elif data[0][1] == user_name and data[0][2] != user_password:
        return render_template("signin.html", warning='密碼錯誤')
    elif data[0][1] == user_name and data[0][2] == user_password:
        return render_template("a.html")


    
# 點擊載入a功能頁面
@app.route("/a", methods=["GET", "POST"])
def a():
    if request.method == 'POST':   # 如果是 POST 請求
        start_date_str = request.form['start_date'] # 2023-05-05  # 從 request.form 取得 start_date 參數
        end_date_str = request.form['end_date']   # 從 request.form 取得 end_date 參數
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')   # 將 start_date_str 字串轉為 datetime 物件
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')   # 將 end_date_str 字串轉為 datetime 物件
        delta = end_date - start_date   # 計算日期區間
        x = [start_date + timedelta(days=i) for i in range(delta.days + 1)]   # 產生日期區間內每一天的日期
        y = [random.randint(0, 100) for _ in range(delta.days + 1)]   # 產生一個數值列表，該列表長度與日期區間相同
        fig = go.Figure()   # 建立一個 plotly 的 Figure 物件
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))   # 在 Figure 物件中添加一個 Scatter 圖形
        fig.update_layout(title=f'日期區間: {start_date_str} - {end_date_str}', xaxis_title='日期', yaxis_title='Value')   # 更新 Figure 物件的布
        # 将图表转换为HTML文件
        div = opy.plot(fig, auto_open=False, output_type='div')

        da = daily_data() #賣場數據總攬
        di = daily_insight() # 賣場警告
        ds = daily_score() # 賣場分數
       
        

        # 回傳 a頁面                         # 這個是圖像介面
        return render_template ("a.html" ,div_placeholder=div, da = da, ds = ds, di = di ) 
     # 如果是 GET 請求
    else:
        return render_template("a.html")
       

# 點擊載入b功能頁面
@app.route("/b", methods=["GET"])
def b():
    kpi1 = "kpi"
    return render_template("b.html", kpi1=kpi1)

# 點擊載入c功能頁面
@app.route("/c", methods=["GET"])
def c():
    
    gre = growth_rate_error()
    gre1 = list(gre.values())
    app.logger.debug(gre1)
    app.logger.debug("==============================================")
    

    return render_template("c.html"   ,gre1 = gre1)

# 點擊載入d功能頁面
@app.route("/d", methods=["GET","POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    # ====================第一張圖:[點擊每月按鈕] 賣場資訊(柱狀圖)_START======================                         
    if request.form.get('button') == '5':
        start = request.form.get('start')
        end = request.form.get('end')
        dataset = SQLcommand().get(f'SELECT shop_name AS name, SUM(fans_count) AS fans, SUM(rating_counts) AS rating FROM offical_data WHERE date>="{start}" AND date<="{end}" GROUP BY name ORDER BY fans DESC')
        x, y, y2 = [element[0] for element in dataset], [element[1] for element in dataset], [element[2] for element in dataset]
        chart_html = DrawChart().bar('競品總覽', '商店名稱', '粉絲數', '評價數', x, y, y2)
        return render_template('index.html', chart_html=chart_html)

    # ===========第二張圖:評價數(折線圖)_start================= 

    if request.form.get('button') == '10':
        start = request.form.get('start')
        end = request.form.get('end')
        dataset = SQLcommand().get(f'SELECT date, shop_name AS name, rating_counts AS rating FROM offical_data WHERE date >= "{start}" AND date <= "{end}"')
        
        # 整理數據
        x_data = {}  # 用於存儲每個商家對應的時間數據
        y_data = {}  # 用於存儲每個商家的銷售額數據

    for row in dataset:
        date = row[0]
        shop_name = row[1]
        rating = row[2]
        if shop_name not in x_data:
            x_data[shop_name] = []
            x_data[shop_name].append(date)
            # 添加銷售額數據到 y_data 字典
        if shop_name not in y_data:
            y_data[shop_name] = []  
        y_data[shop_name].append(rating)

        # 調用 lines_times 函式
        chart_html = DrawChart().lines_times("評價數趨勢圖", "日期", "評價數", x_data, y_data)
        return render_template("index.html", chart_html=chart_html)

    # ===========評價數_end================= 

    # ===========第三張圖:粉絲數(折線圖)_start=================
    if request.form.get('button') == 'line':
        start = request.form.get('start')
        end = request.form.get('end')
        dataset = SQLcommand().get(f'SELECT date, shop_name AS name, fans_count AS fans FROM offical_data WHERE date>="{start}" AND date<="{end}" ORDER BY fans DESC')

    # 整理數據
    x_data = {}  # 用於存儲每個商家對應的時間數據
    y_data = {}  # 用於存儲每個商家的銷售額數據

    for row in dataset:
        date = row[0]
        shop_name = row[1]
        fans = row[2]
        if shop_name not in x_data:
            x_data[shop_name] = []
        x_data[shop_name].append(date)
        # 添加銷售額數據到 y_data 字典
        if shop_name not in y_data:
            y_data[shop_name] = []
        y_data[shop_name].append(fans)

    # 調用 lines_times 函式
        chart_html = DrawChart().lines_times("粉絲數趨勢圖", "日期", "粉絲數", x_data, y_data)
        return render_template("index.html", chart_html=chart_html)

    # ===========粉絲數_end=================

    # =====================第四張圖:日銷售額(折線圖)_START======================

    if request.form.get('button') == 'bar':
        start = request.form.get('start')
        end = request.form.get('end') 

        dataset = SQLcommand().get(f'SELECT shop_name AS name, DATE_FORMAT(date, "%Y-%m-%d") AS sales_day, SUM(monthly_sales * price) AS daily_sales FROM products_info WHERE date>="{start}" AND date<="{end}" GROUP BY name, sales_day')
        my_dataset = SQLcommand().get(f'SELECT shop_name AS name, DATE_FORMAT(date, "%Y-%m-%d") AS sales_day, daily_sales AS daily_sales FROM my_products_info WHERE date>="{start}" AND date<="{end}"')


        line_data = {}

        for element in dataset:
            date = datetime.strptime(element[1], "%Y-%m-%d")
            shop_name = element[0]
            sales = element[2]
            if shop_name not in line_data:
                line_data[shop_name] = {}
            line_data[shop_name][date] = {"sales": sales, "source": "dataset"}

        for my_elements in my_dataset:
            date = datetime.strptime(my_elements[1], "%Y-%m-%d")
            my_shop_name=my_elements[0]
            my_sales=my_elements[2]
            if my_shop_name not in line_data:
                line_data[my_shop_name] = {}
            line_data[my_shop_name][date] = {"sales": my_sales, "source": "my_dataset"}

        # Set the date range based on the user input
        date_range = pd.date_range(start=start, end=end)
        x = [date.strftime('%Y-%m-%d') for date in date_range]

        y_data = {}

        for shop_name, data in line_data.items():
            y_data[shop_name] = []
            if shop_name == '宅栽工作室':
                for date in date_range:
                    current_sales = data.get(date, {"sales": 0})["sales"]
                    y_data[shop_name].append(current_sales)
            else:
                previous_sales = 0
                for date in date_range:
                    current_sales = data.get(date, {"sales": 0})["sales"]
                    sales_diff = current_sales - previous_sales
                    previous_sales = current_sales
                    y_data[shop_name].append(sales_diff)

        chart_html = DrawChart().lines7('月銷售額','年月份','銷售變動', x, y_data)
        return render_template('index.html', chart_html=chart_html)
    

# 點擊載入e功能頁面
@app.route("/e", methods=["GET", "POST"])
def e():
    if request.method == 'GET':
        return render_template("e.html")
    clear_folder('static/photos/')
    text = []
    files = request.files.getlist('file')
    print(len(files))
    if len(files) == 4 and files[0].filename:
        warning = ''
        for file in files:
            file.save('static/photos/' + file.filename)
            evaluate = predict_image(f'static/photos/{file.filename}')
            text.append({'picture': f'static/photos/{file.filename}', 'score': evaluate})
    else: warning = '請選擇4張圖片'
    return render_template('e.html', scores=text, warning=warning)

# 讓程式跑起來
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")