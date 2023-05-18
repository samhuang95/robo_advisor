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
  
  # if request.form.get('options'):
  #   value = request.form.get('options')
  #   dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM facebook_posts WHERE MONTH(time) = {value} AND YEAR(time) = 2023 ORDER BY time')
  #   data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
  #   return render_template('index.html', message=f'2023年{value}月', data=data_dict, selected_value=value)
  
                           
  if request.form.get('button') == 'date':
    start = request.form.get('start')
    end = request.form.get('end')
    dataset = SQLcommand().get(f'SELECT shop_name AS name, SUM(fans_count) AS fans, SUM(rating_counts) AS rating FROM offical_data WHERE date>="{start}" AND date<="{end}" GROUP BY name ORDER BY fans DESC')
    x, y, y2 = [element[0] for element in dataset], [element[1] for element in dataset], [element[2] for element in dataset]
    chart_html = DrawChart().bar('競品總覽', '商店名稱', '粉絲數', '評價數', x, y, y2)
    return render_template('index.html', chart_html=chart_html)
  


  if request.form.get('button') == 'date':
    start = request.form.get('start')
    end = request.form.get('end')
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    if start_date < end_date:
      return render_template('test.html', start=start, end=end)
    else:
      return render_template('index.html', message='結束日期不能早於開始日期！')
  
  # if request.form.get('button') == 'login':
  #   account = request.form.get('account')
  #   password = request.form.get('password')
  #   return render_template('test.html', start=account, end=password)

  # value = request.form.get('button')
  # dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM facebook_posts ORDER BY time DESC LIMIT {value}')
  # data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
  # return render_template('index.html', message=f'資料庫前{value}筆資料', data=data_dict)


if __name__ == '__main__':
  app.run(host='0.0.0.0')
