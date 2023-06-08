from datetime import datetime, timedelta
from flask import Flask, render_template, request, session
from functions.store_overview.store_overview import *
from functions.store_overview.goal import *
from functions.connect_to_db import SQLcommand
from functions.image_predict import predict_image
from functions.clear_folder import clear_folder
# from BCG_funtions import *
import logging
from page_b import page_b
from BCG_funtions import *


# ==============德瑈功能
from competitor_draw_chart import DrawChart
from datetime import timedelta, datetime, date as dt_date
from datetime import datetime, timedelta



app=Flask(__name__)
app.secret_key = 'your_secret_key'
logging.basicConfig(level=logging.DEBUG)


app.register_blueprint(page_b)


# 做一個註冊的路由
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    user_name = request.form['user_name']
    # session['username'] = username
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
    # session['username'] = username
    user_password = request.form['user_password']
    today = "2023-05-31"
    # today = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    data = SQLcommand().get(f'SELECT * FROM user_data WHERE account = "{user_name}"')
    if not data:
        return render_template("signin.html", warning='請註冊帳號')
    elif data[0][1] == user_name and data[0][2] != user_password:
        return render_template("signin.html", warning='密碼錯誤')
    elif data[0][1] == user_name and data[0][2] == user_password:
        session['username'] = user_name
        line_chart  = line_stack_area(today)
        chart_html = line_chart.render_embed()
        da = daily_data(today) #賣場數據總攬
        di = daily_insight(today) # 賣場警告
        ds = daily_score(today) # 賣場分數
        # 回傳 a頁面                         # 這個是圖像介面
        return render_template ("a.html" , da = da, di=di,ds=ds,chart_html = chart_html, today=today, start_date_str = today) 
        # return render_template("a.html")


    
# 點擊載入a功能頁面
@app.route("/effectiveness", methods=["GET", "POST"])
def effectivenessa():
    today = "2023-05-31"
    # today = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    if request.method == 'POST':   # 如果是 POST 請求
        start_date_str = request.form['start_date'] # 2023-05-05  # 從 request.form 取得 start_date 參數
        line_chart  = line_stack_area(start_date_str)
        chart_html = line_chart.render_embed()
        da = daily_data(start_date_str) #賣場數據總攬
        di = daily_insight(start_date_str) # 賣場警告
        ds = daily_score(start_date_str) # 賣場分數
        # 回傳 a頁面                         # 這個是圖像介面
        return render_template ("a.html" , da = da, di=di,ds=ds,chart_html = chart_html, today=today, start_date_str=start_date_str) 
     # 如果是 GET 請求
    else:
        line_chart  = line_stack_area(today)
        chart_html = line_chart.render_embed()
        da = daily_data(today) #賣場數據總攬
        di = daily_insight(today) # 賣場警告
        ds = daily_score(today) # 賣場分數
        # 回傳 a頁面                         # 這個是圖像介面
        return render_template ("a.html" , da = da, di=di,ds=ds,chart_html = chart_html, today=today, start_date_str = today) 
       

# 點擊載入b功能頁面
# @app.route("/b", methods=["GET"])
# def b():
#     kpi1 = "kpi"
#     return render_template("b.html", kpi1=kpi1)

# 點擊載入c功能頁面
@app.route("/execution", methods=["GET" , "POST"])
def execution():
    today = datetime.today().strftime('%Y-%m')
    if request.method == 'GET':
        ih = inventory_highlight()
        ih_list = list(ih.values())
        return render_template("c.html", ih_list = ih_list, start_month_str=today)
    if request.method == 'POST':   # 如果是 POST 請求
        start_month_str = request.form['start_date']
        ih = inventory_highlight()
        ih_list = list(ih.values())
        return render_template("c.html", ih_list = ih_list , start_month_str=start_month_str)

# 點擊載入d功能頁面
@app.route("/datamonitoring", methods=["GET","POST"])
def datamonitoring():
    if request.method == 'GET':
        today = datetime.today().date()
        start_date = today - timedelta(days=20)  # 從今天起回溯10天

        # 使用 SQL 查詢獲取最近一次有資料的日期
        last_data_date = SQLcommand().get(f"""
            SELECT MAX(DATE(date_time)) AS last_date
            FROM product_detail;
        """)[0][0]

        if last_data_date:
            end_date = min(today - timedelta(days=1), last_data_date)
        else:
            end_date = today - timedelta(days=1)  # 不包含今天

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        my_dataset = SQLcommand().get(f"""
            SELECT MAX(DATE_FORMAT(date_time, "%Y-%m-%d")) AS sales_day, SUM(total_sales) AS daily_sales
            FROM product_detail
            WHERE date_time >= "{start_date_str}" AND date_time <= "{end_date_str}"
            GROUP BY DATE_FORMAT(date_time, "%Y-%m-%d");
        """)

        dataset = SQLcommand().get(f"""
            SELECT
                sub.name,
                sub.sales_day,
                sub.daily_sales
            FROM (
                SELECT
                    p1.shop_name AS name,
                    MAX(DATE_FORMAT(p1.date, "%Y-%m-%d")) AS sales_day,
                    SUM(
                        CASE
                            WHEN (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) >= 0 THEN (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales)
                            ELSE 0
                        END
                    ) AS daily_sales
                FROM
                    products_info p1
                LEFT JOIN products_info p2 ON p1.product_id = p2.product_id
                    AND DATE_FORMAT(p1.date, "%Y-%m-%d") = DATE_FORMAT(DATE_ADD(p2.date, INTERVAL 1 DAY), "%Y-%m-%d")
                WHERE 
                    p1.date >= "{start_date_str}" AND p1.date <= "{end_date_str}"
                    AND p1.historical_sales >= p2.historical_sales
                    AND (p1.historical_sales - p2.historical_sales) < 10
                    AND (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) <= 5000
                    AND (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) >= 0 
                GROUP BY
                    p1.shop_name,
                    DATE_FORMAT(p1.date, "%Y-%m-%d")
                HAVING
                    MIN((p1.price * p1.historical_sales) - (p1.price * p2.historical_sales)) >= 0 
            ) AS sub;
        """)

        line_data = {}

        for element in dataset:
            date = datetime.strptime(element[1], "%Y-%m-%d")
            shop_name = element[0]
            sales = max(element[2], 0)
            if shop_name not in line_data:
                line_data[shop_name] = {}
            line_data[shop_name][date] = {"sales": sales, "source": "dataset"}

        for my_elements in my_dataset:
            date = datetime.strptime(my_elements[0], "%Y-%m-%d")
            my_shop_name = "宅栽工作室"
            my_sales = my_elements[1]
            if my_shop_name not in line_data:
                line_data[my_shop_name] = {}
            line_data[my_shop_name][date] = {"sales": my_sales, "source": "my_dataset"}

        # 設定日期範圍
        date_range = pd.date_range(start=start_date, end=end_date)
        x = [date.strftime('%Y-%m-%d') for date in date_range]

        y_data = {
            "宅栽工作室": [],
            "麗都花園": [],
            "珍奇植物": [],
            "開心農元": [],
            "糀町植葉": [],
            "沐時園藝": [],
            "小李植栽": [],
            "南犬植栽": []
        }

        for shop_name, data in line_data.items():
            y_data[shop_name] = []
            for date in date_range:
                current_sales = data.get(date, {"sales": 0})["sales"]
                y_data[shop_name].append(current_sales)

        chart_html = DrawChart().lines7('日銷售額', '年月份', '銷售金額', x, y_data)
        return render_template("index.html", chart_html=chart_html)

    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        button_value = request.form.get('button')

        if button_value == '5': 
            dataset = SQLcommand().get(f'''SELECT shop_name AS name, SUM(fans_count) AS fans, SUM(rating_counts) AS rating
                FROM offical_data
                WHERE date = (
                    SELECT MAX(date)
                    FROM offical_data
                    WHERE date <= "{end}"
                )
                GROUP BY name
                ORDER BY CASE WHEN name = "宅栽工作室" THEN 0 ELSE 1 END, name != "宅栽工作室", fans DESC
                ''')
            x, y, y2 = [element[0] for element in dataset], [element[1] for element in dataset], [element[2] for element in dataset]
            chart_html = DrawChart().bar('競品總覽', '商店名稱', '粉絲數', '評價數', x, y, y2)
            return render_template('index.html', chart_html=chart_html)

        elif button_value == '10':
            dataset = SQLcommand().get(f'SELECT date, shop_name AS name, rating_counts AS rating FROM offical_data WHERE date >= "{start}" AND date <= "{end}" ORDER BY date')
            x_data = {}  
            y_data = {"宅栽工作室":[],"麗都花園":[],"珍奇植物":[],"開心農元":[],"糀町植葉":[],"沐時園藝":[],"小李植栽":[],"南犬植栽":[]}

            for row in dataset:
                date = row[0]
                shop_name = row[1]
                rating = row[2]
                if shop_name not in x_data:
                    x_data[shop_name] = []
                x_data[shop_name].append(date)
                y_data[shop_name].append(rating)

            # 調用 lines_times 函式
            chart_html = DrawChart().lines_times("評價趨勢", "日期", "評價數", x_data, y_data)
            # print(x_data)
            return render_template("index.html", chart_html=chart_html)
        

        elif button_value == 'line':
            dataset = SQLcommand().get(f'SELECT date, shop_name AS name, fans_count AS fans FROM offical_data WHERE date>="{start}" AND date<="{end}" ORDER BY date')
            x_data = {}  
            y_data = {"宅栽工作室":[],"麗都花園":[],"珍奇植物":[],"開心農元":[],"糀町植葉":[],"沐時園藝":[],"小李植栽":[],"南犬植栽":[]}

            for row in dataset:
                date = row[0]
                shop_name = row[1]
                fans = row[2]
                if shop_name not in x_data:
                    x_data[shop_name] = []
                x_data[shop_name].append(date)
                if shop_name not in y_data:
                    y_data[shop_name] = []
                y_data[shop_name].append(fans)
            chart_title = "粉絲趨勢"
            chart_html = DrawChart().lines_times(chart_title, "日期", "粉絲數", x_data, y_data)
            return render_template("index.html", chart_title=chart_title, chart_html=chart_html)

        elif button_value == 'bar':
            my_dataset = SQLcommand().get(f"""SELECT DATE_FORMAT(date_time, "%Y-%m-%d") AS sales_day, SUM(total_sales) AS daily_sales FROM product_detail WHERE date_time >="{start}" AND date_time<="{end}"
                                        GROUP BY DATE_FORMAT(date_time, "%Y-%m-%d");""")
            dataset = SQLcommand().get(f"""
            SELECT
                sub.name,
                sub.sales_day,
                sub.daily_sales
            FROM (
                SELECT
                    p1.shop_name AS name,
                    DATE_FORMAT(p1.date, "%Y-%m-%d") AS sales_day,
                    SUM(
                        CASE
                            WHEN (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) >= 0 THEN (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales)
                            ELSE 0
                        END
                    ) AS daily_sales
                FROM
                    products_info p1
                LEFT JOIN products_info p2 ON p1.product_id = p2.product_id
                    AND DATE_FORMAT(p1.date, "%Y-%m-%d") = DATE_FORMAT(DATE_ADD(p2.date, INTERVAL 1 DAY), "%Y-%m-%d")
                WHERE
                    DATE_FORMAT(p1.date, "%Y-%m-%d") BETWEEN "{start}" AND "{end}"
                    AND p1.historical_sales >= p2.historical_sales
                    AND (p1.historical_sales - p2.historical_sales) < 10
                    AND (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) <= 5000
                    AND (p1.price * p1.historical_sales) - (p1.price * p2.historical_sales) >= 0 
                GROUP BY
                    p1.shop_name,
                    DATE_FORMAT(p1.date, "%Y-%m-%d")
                HAVING
                    MIN((p1.price * p1.historical_sales) - (p1.price * p2.historical_sales)) >= 0 
            ) AS sub;

            """)

            line_data = {}

            for element in dataset:
                date = datetime.strptime(element[1], "%Y-%m-%d")
                shop_name = element[0]
                sales = max(element[2],0)
                if shop_name not in line_data:
                    line_data[shop_name] = {}
                line_data[shop_name][date] = {"sales": sales, "source": "dataset"}
            print(my_dataset)
            for my_elements in my_dataset:
                date = datetime.strptime(my_elements[0], "%Y-%m-%d")
                my_shop_name="宅栽工作室"
                print(my_shop_name)
                my_sales=my_elements[1]
                if my_shop_name not in line_data:
                    line_data[my_shop_name] = {}
                line_data[my_shop_name][date] = {"sales": my_sales, "source": "my_dataset"}
            # Set the date range based on the user input
            date_range = pd.date_range(start=start, end=end)
            x = [date.strftime('%Y-%m-%d') for date in date_range]

            y_data = {"宅栽工作室":[],"麗都花園":[],"珍奇植物":[],"開心農元":[],"糀町植葉":[],"沐時園藝":[],"小李植栽":[],"南犬植栽":[]}

            for shop_name, data in line_data.items():
                y_data[shop_name] = []
                for date in date_range:
                    current_sales = data.get(date, {"sales": 0})["sales"]
                    y_data[shop_name].append(current_sales)

            chart_html = DrawChart().lines7('日銷售額','年月份','銷售金額', x, y_data)
            return render_template("index.html", chart_html=chart_html)
            



    # ====================第一張圖:[點擊每月按鈕] 賣場資訊(柱狀圖)_START======================                         
    # if request.form.get('button') == '5':
    #     start = request.form.get('start')
    #     end = request.form.get('end')
    #     dataset = SQLcommand().get(f'SELECT shop_name AS name, SUM(fans_count) AS fans, SUM(rating_counts) AS rating FROM offical_data WHERE date>="{start}" AND date<="{end}" GROUP BY name ORDER BY fans DESC')
    #     x, y, y2 = [element[0] for element in dataset], [element[1] for element in dataset], [element[2] for element in dataset]
    #     chart_html = DrawChart().bar('競品總覽', '商店名稱', '粉絲數', '評價數', x, y, y2)
    #     return render_template('index.html', chart_html=chart_html)

    # ===========第二張圖:評價數(折線圖)_start================= 

    # if request.form.get('button') == '10':
    #     start = request.form.get('start')
    #     end = request.form.get('end')
    #     dataset = SQLcommand().get(f'SELECT date, shop_name AS name, rating_counts AS rating FROM offical_data WHERE date >= "{start}" AND date <= "{end}"')
        
    #     # 整理數據
    #     x_data = {}  # 用於存儲每個商家對應的時間數據
    #     y_data = {}  # 用於存儲每個商家的銷售額數據

    # for row in dataset:
    #     date = row[0]
    #     shop_name = row[1]
    #     rating = row[2]
    #     if shop_name not in x_data:
    #         x_data[shop_name] = []
    #         x_data[shop_name].append(date)
    #         # 添加銷售額數據到 y_data 字典
    #     if shop_name not in y_data:
    #         y_data[shop_name] = []  
    #     y_data[shop_name].append(rating)

    #     # 調用 lines_times 函式
    #     chart_html = DrawChart().lines_times("評價數趨勢圖", "日期", "評價數", x_data, y_data)
    #     return render_template("index.html", chart_html=chart_html)

    # ===========評價數_end================= 

    # ===========第三張圖:粉絲數(折線圖)_start=================
    # if request.form.get('button') == 'line':
    #     start = request.form.get('start')
    #     end = request.form.get('end')
    #     dataset = SQLcommand().get(f'SELECT date, shop_name AS name, fans_count AS fans FROM offical_data WHERE date>="{start}" AND date<="{end}" ORDER BY fans DESC')

    # # 整理數據
    # x_data = {}  # 用於存儲每個商家對應的時間數據
    # y_data = {}  # 用於存儲每個商家的銷售額數據

    # for row in dataset:
    #     date = row[0]
    #     shop_name = row[1]
    #     fans = row[2]
    #     if shop_name not in x_data:
    #         x_data[shop_name] = []
    #     x_data[shop_name].append(date)
    #     # 添加銷售額數據到 y_data 字典
    #     if shop_name not in y_data:
    #         y_data[shop_name] = []
    #     y_data[shop_name].append(fans)

    # # 調用 lines_times 函式
    #     chart_html = DrawChart().lines_times("粉絲數趨勢圖", "日期", "粉絲數", x_data, y_data)
    #     return render_template("index.html", chart_html=chart_html)

    # # ===========粉絲數_end=================

    # # =====================第四張圖:日銷售額(折線圖)_START======================

    # if request.form.get('button') == 'bar':
    #     start = request.form.get('start')
    #     end = request.form.get('end') 

    #     dataset = SQLcommand().get(f'SELECT shop_name AS name, DATE_FORMAT(date, "%Y-%m-%d") AS sales_day, SUM(monthly_sales * price) AS daily_sales FROM products_info WHERE date>="{start}" AND date<="{end}" GROUP BY name, sales_day')
    #     my_dataset = SQLcommand().get(f'SELECT shop_name AS name, DATE_FORMAT(date, "%Y-%m-%d") AS sales_day, daily_sales AS daily_sales FROM my_products_info WHERE date>="{start}" AND date<="{end}"')


    #     line_data = {}

    #     for element in dataset:
    #         date = datetime.strptime(element[1], "%Y-%m-%d")
    #         shop_name = element[0]
    #         sales = element[2]
    #         if shop_name not in line_data:
    #             line_data[shop_name] = {}
    #         line_data[shop_name][date] = {"sales": sales, "source": "dataset"}

    #     for my_elements in my_dataset:
    #         date = datetime.strptime(my_elements[1], "%Y-%m-%d")
    #         my_shop_name=my_elements[0]
    #         my_sales=my_elements[2]
    #         if my_shop_name not in line_data:
    #             line_data[my_shop_name] = {}
    #         line_data[my_shop_name][date] = {"sales": my_sales, "source": "my_dataset"}

    #     # Set the date range based on the user input
    #     date_range = pd.date_range(start=start, end=end)
    #     x = [date.strftime('%Y-%m-%d') for date in date_range]

    #     y_data = {}

    #     for shop_name, data in line_data.items():
    #         y_data[shop_name] = []
    #         if shop_name == '宅栽工作室':
    #             for date in date_range:
    #                 current_sales = data.get(date, {"sales": 0})["sales"]
    #                 y_data[shop_name].append(current_sales)
    #         else:
    #             previous_sales = 0
    #             for date in date_range:
    #                 current_sales = data.get(date, {"sales": 0})["sales"]
    #                 sales_diff = current_sales - previous_sales
    #                 previous_sales = current_sales
    #                 y_data[shop_name].append(sales_diff)

    #     chart_html = DrawChart().lines7('月銷售額','年月份','銷售變動', x, y_data)
        # return render_template('index.html', chart_html=chart_html)
    

# 點擊載入e功能頁面
@app.route('/FBdata', methods=['GET', 'POST'])
def e():
    if request.method == 'GET':
        return render_template("e.html")

    clear_folder('static/photos/')

    files = request.files.getlist('file')

    if not files[0].filename:
        return render_template('e.html', warning='請選擇至少1張圖片')

    elif len(files) > 4:
        return render_template('e.html', warning='請選擇少於4張圖片')

    else:
        text = []
        for file in files:
            file.save('static/photos/' + file.filename)
            evaluate = predict_image(f'static/photos/{file.filename}')
            text.append({'picture': f'static/photos/{file.filename}', 'score': evaluate})

        return render_template('e.html', scores=text, num=len(text))

# 讓程式跑起來
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")