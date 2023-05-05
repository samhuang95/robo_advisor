from flask import Flask, render_template, request
from functions.connect_to_db import SQLcommand
from functions.draw_chart import DrawChart

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  return render_template('index.html', message='Hello Flask!')

@app.route('/1')
def template1():
  return render_template('template1.html')

@app.route('/2')
def template2():
  return render_template('template2.html')

@app.route('/3')
def template3():
  return render_template('template3.html')

@app.route('/4')
def template4():
  return render_template('template4.html')

@app.route('/5')
def template5():
  return render_template('template5.html')

@app.route('/', methods=['POST'])
def submit():
  if request.form.get('options'):
    value = request.form.get('options')
    dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM posts WHERE MONTH(time) = {value} AND YEAR(time) = 2023 ORDER BY time')
    data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
    return render_template('index.html', message=f'2023年{value}月', data=data_dict, selected_value=value)

  if request.form.get('button') == 'line':
    dataset = SQLcommand().get('SELECT DATE_FORMAT(time, "%Y") AS year, COUNT(*) FROM posts GROUP BY year ORDER BY year')
    x, y = [element[0] for element in dataset], [element[1] for element in dataset]
    chart_html = DrawChart().line('Posts of Year', 'Year', 'Posts', x, y)
    return render_template('index.html', chart_html=chart_html)
  
  if request.form.get('button') == 'bar':
    dataset = SQLcommand().get('SELECT DATE_FORMAT(time, "%Y") AS year, COUNT(*) FROM posts GROUP BY year ORDER BY year')
    x, y = [element[0] for element in dataset], [element[1] for element in dataset]
    chart_html = DrawChart().bar('Posts of Year', 'Year', 'Posts', x, y)
    return render_template('index.html', chart_html=chart_html)

  value = request.form.get('button')
  dataset = SQLcommand().get(f'SELECT time, likes, reactions, shares, comments FROM posts ORDER BY time DESC LIMIT {value}')
  data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in dataset]
  return render_template('index.html', message=f'資料庫前{value}筆資料', data=data_dict)

if __name__ == '__main__':
  app.run(host='0.0.0.0')