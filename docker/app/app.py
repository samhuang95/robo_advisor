from datetime import datetime, timedelta
from flask import Flask, render_template, request
from functions.connect_to_db import SQLcommand
# from functions.image_predict import predict_image
from functions.clear_folder import clear_folder
import random   # 匯入 random 模組
import plotly.graph_objs as go   # 匯入 plotly.graph_objs 模組並使用 go 簡寫
import plotly.offline as opy
from functions.store_overview.store_overview import *

app=Flask(__name__)

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
        start_date_str = request.form['start_date']   # 從 request.form 取得 start_date 參數
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
    c = {
        "a":"a_優先處裡植物",
        "b":"b_優先處裡植物",
        "c":"c_優先處裡植物",
        "d":"d_優先處裡植物",
        "e":"e_優先處裡植物",
    }
    return render_template("c.html" , c=c)

# 點擊載入d功能頁面
@app.route("/d", methods=["GET"])
def d():
    return render_template("d.html")

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