from flask import Flask, render_template, request
from connect_to_sql import SQLCommand
from draw_chart import DrawChart

app = Flask(__name__)
app.debug = True
app.config

@app.route('/')
def index():
  return render_template('index.html', message='Hello Flask!')

@app.route('/', methods=['POST'])
def submit():
  if request.form.get('options'):
    value = request.form.get('options')
    table = SQLCommand().get(f'SELECT time, likes, reactions, shares, comments FROM posts WHERE MONTH(time) = {value} AND YEAR(time) = 2023 ORDER BY time')
    data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in table]
    return render_template('index.html', message=f'2023年{value}月', data=data_dict, selected_value=value)

  if request.form.get('button') == 'line':
    table = SQLCommand().get('SELECT DATE_FORMAT(time, "%Y") AS year, COUNT(*) FROM posts GROUP BY year ORDER BY year')
    x, y = [element[0] for element in table], [element[1] for element in table]
    DrawChart().line(x, y, app.root_path)
    return render_template('index.html', chart='line')
  
  if request.form.get('button') == 'bar':
    table = SQLCommand().get('SELECT DATE_FORMAT(time, "%Y") AS year, COUNT(*) FROM posts GROUP BY year ORDER BY year')
    x, y = [element[0] for element in table], [element[1] for element in table]
    DrawChart().bar(x, y, app.root_path)
    return render_template('index.html', chart='bar')

  value = request.form.get('button')
  table = SQLCommand().get(f'SELECT time, likes, reactions, shares, comments FROM posts ORDER BY time DESC LIMIT {value}')
  data_dict = [{'time': data[0], 'likes': data[1], 'reactions': data[2], 'shares': data[3], 'comments': data[4]} for data in table]
  return render_template('index.html', message=f'資料庫前{value}筆資料', data=data_dict)

if __name__ == '__main__':
  app.run(host='0.0.0.0')