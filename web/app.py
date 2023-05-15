# import 所需資料
from datetime import datetime, timedelta   # 匯入 datetime 和 timedelta 模組
import random   # 匯入 random 模組
import plotly.graph_objs as go   # 匯入 plotly.graph_objs 模組並使用 go 簡寫
import plotly.offline as opy


# 初始化 Flask 伺服器 呼叫flask全部功能
from flask import *

# 路徑
app=Flask(__name__,
          static_folder="public",
          static_url_path="/"
)

# 跟mysql資料庫連結
from flask_sqlalchemy import SQLAlchemy
import pymysql
import traceback
# 將金鑰放到json檔裡面不要讓他放在一起
import json
with open('sql.json','r',encoding="utf-8") as s:
        jdata = json.load(s)

# 連接資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = jdata["mysql"]
print(jdata["mysql"])
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Asdf0978932728@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 做一個member的class
class Member(db.Model):
    __tablename__ = 'member'
    user_email = db.Column(db.String(255), primary_key=True)
    user_name = db.Column(db.String(255))
    user_password = db.Column(db.String(255))

# 設至權限
app.secret_key="any string  but secret"

# 做一個有登入跟去註冊網頁的畫面 路由
@app.route("/")
def project01():
    return render_template("project01.html")

# 做一個首頁的路由
# @app.route("/index")
# def index():
#     return render_template("index.html")

# 做一個錯誤的路由
@app.route("/error")
def error():
    message=request.args.get("msg","發生錯請聯繫客服")
    return render_template("error.html", message=message)

# 登入路徑
@app.route("/singup1")
def singup01():
    return render_template("singup.html")

# 做一個註冊的路由
@app.route("/singup", methods=["POST"])
def singup():
    user_email = request.form['user_email']
    user_name = request.form['user_name']
    user_password = request.form['user_password']
    # 根據接收到的資料, 和資料庫作互動
     # 檢查使用者電子郵件是否已經存在
    existing_email = Member.query.filter_by(user_email=user_email).first()
    if existing_email:
        return "此user_email已經有人使用"

    # 檢查使用者密碼是否已經存在
    existing_password = Member.query.filter_by(user_password=user_password).first()
    if existing_password:
        return "此user_password已經有人使用"
    # 創建新會員並儲存到資料庫
    new_member = Member(user_email=user_email, user_name=user_name, user_password=user_password)
    db.session.add(new_member)
    db.session.commit()

    return render_template("project01.html")
# 做一個登入的路由
@app.route("/singin", methods=["POST"])
def singin():
        user_email = request.form['user_email']
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        
        member = Member.query.filter_by(user_email=user_email, user_name=user_name, user_password=user_password).first()
        print(member.user_name)
        if member == None:
            return "請註冊"
        
        return render_template("a.html")
    
# 點擊載入a功能頁面
@app.route("/a", methods=["GET", 'POST'])
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
        # 銷售額,成交量,商品瀏覽數,訪客數
        a = {
                "sales" : "銷售額",
                "turnover": "成交量",
                "Product_Views": "商品瀏覽數",
                "number_of_visitors": "訪客數",
                "a_highlight": "a_highlight",
                "b_highlight": "b_highlight",
                "c_highlight": "c_highlight",
                "d_highlight": "d_highlight",
                "e_highlight": "e_highlight",
            }
        

        # 回傳 a頁面                         # 這個是圖像介面
        return render_template ("a.html" ,div_placeholder=div, a = a) 
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
@app.route("/e", methods=["GET"])
def e():
    return render_template("e.html")




@app.route("/head")
def head():
    return render_template("project01.html")

# 讓程式跑起來
app.run(debug=True, host="0.0.0.0",port=3000)