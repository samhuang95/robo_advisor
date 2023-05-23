from flask import Flask, render_template, request
from functions.connect_to_db import SQLcommand
from functions.draw_chart import DrawChart
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html', message='Hello Flask!')

  # ====================第一張圖:[點擊每月按鈕] 賣場資訊(柱狀圖)_START======================                         
  if request.form.get('button') == 'date':
    start = request.form.get('start')
    end = request.form.get('end')
    dataset = SQLcommand().get(f'SELECT shop_name AS name, SUM(fans_count) AS fans, SUM(rating_counts) AS rating FROM offical_data WHERE date>="{start}" AND date<="{end}" GROUP BY name ORDER BY fans DESC')
    x, y, y2 = [element[0] for element in dataset], [element[1] for element in dataset], [element[2] for element in dataset]
    chart_html = DrawChart().bar('競品總覽', '商店名稱', '粉絲數', '評價數', x, y, y2)
    return render_template('index.html', chart_html=chart_html)
  
# ===========第二張圖:評價數(折線圖)_start================= 

  if request.form.get('button') == 'date':
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
  if request.form.get('button') == 'date':
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

  if request.form.get('button') == 'date':
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
  # ===========日銷售額_END=================

# ==========僅供參考區(非畫圖)==========================
# if request.form.get('button') == 'login':
  #   account = request.form.get('account')
  #   password = request.form.get('password')
  #   return render_template('test.html', start=account, end=password)

  # value = request.form.get('button')
  # dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM facebook_posts ORDER BY time DESC LIMIT {value}')
  # data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
  # return render_template('index.html', message=f'資料庫前{value}筆資料', data=data_dict)


  # if request.form.get('button') == 'date':
  #   start = request.form.get('start')
  #   end = request.form.get('end')
  #   start_date = datetime.strptime(start, '%Y-%m-%d')
  #   end_date = datetime.strptime(end, '%Y-%m-%d')
  #   if start_date < end_date:
  #     return render_template('test.html', start=start, end=end)
  #   else:
  #     return render_template('index.html', message='結束日期不能早於開始日期！')

    # if request.form.get('options'):
  #   value = request.form.get('options')
  #   dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM facebook_posts WHERE MONTH(time) = {value} AND YEAR(time) = 2023 ORDER BY time')
  #   data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
  #   return render_template('index.html', message=f'2023年{value}月', data=data_dict, selected_value=value)
  
    
if __name__ == '__main__':
  app.run(host='0.0.0.0')
