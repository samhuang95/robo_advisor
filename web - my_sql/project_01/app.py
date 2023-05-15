# import 所需資料
from datetime import datetime, timedelta   # 匯入 datetime 和 timedelta 模組
import random   # 匯入 random 模組
import plotly.graph_objs as go   # 匯入 plotly.graph_objs 模組並使用 go 簡寫

# 連接資料庫
import pymongo
client=pymongo.MongoClient("mongodb+srv://root:root123@cluster0.8rnkov6.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
print("資料庫連線新增成功")

# 初始化 Flask 伺服器 呼叫flask全部功能
from flask import *
# 路徑
app=Flask(__name__,
          static_folder="public",
          static_url_path="/"
)
# 設至權限
app.secret_key="any string  but secret"

# 做一個有登入跟去註冊網頁的畫面 路由
@app.route("/")
def project01():
    return render_template("project01.html")

# 做一個首頁的路由
@app.route("/index")
def index():
    return render_template("index.html")

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
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]
    # 根據接收到的資料, 和資料庫作互動
    collection=db.user
    # 檢查會員集合中是否有相同的 Email 的文件資料
    result=collection.find_one({
        "email":email
    })
    # 判斷有沒有相同資料在裡面
    if result != None:
        return redirect("/error?msg=信箱已經有人使用")
    # 把資料放進資料庫,完成註冊
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

# 做一個登入的路由
@app.route("/singin", methods=["POST"])
def singin():
    #從前端取得使用者的輸入
    email=request.form["email"]
    password=request.form["password"]
    # 和資料庫作互動
    collection=db.user
    # 檢查信箱是否正確
    result=collection.find_one({
        "$and":[
        {"email":email},
        {"password":password}
        ]})
    # 判斷資料庫裡面有無相對應的資料
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功,在 Session 紀錄會員資訊,導向到會員的頁面 權限的管理
    session["nickname"]=result["nickname"]
    return redirect("/index")

# 點擊載入a功能頁面
@app.route("/a", methods=["GET"])
def a():
    return render_template("a.html")

# a頁面功能
@app.route('/plot', methods=['GET', 'POST'])   # 路由定義為 /plot，支援 GET 和 POST 方法
def plot():
    if request.method == 'POST':   # 如果是 POST 請求
        start_date_str = request.form['start_date']   # 從 request.form 取得 start_date 參數
        end_date_str = request.form['end_date']   # 從 request.form 取得 end_date 參數
    else:   # 如果是 GET 請求
        start_date_str = request.args.get('start_date')   # 從 request.args 取得 start_date 參數
        end_date_str = request.args.get('end_date')   # 從 request.args 取得 end_date 參數
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')   # 將 start_date_str 字串轉為 datetime 物件
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')   # 將 end_date_str 字串轉為 datetime 物件
    delta = end_date - start_date   # 計算日期區間
    x = [start_date + timedelta(days=i) for i in range(delta.days + 1)]   # 產生日期區間內每一天的日期
    y = [random.randint(0, 100) for _ in range(delta.days + 1)]   # 產生一個數值列表，該列表長度與日期區間相同
    fig = go.Figure()   # 建立一個 plotly 的 Figure 物件
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))   # 在 Figure 物件中添加一個 Scatter 圖形
    fig.update_layout(title=f'日期區間: {start_date_str} - {end_date_str}', xaxis_title='Date', yaxis_title='Value')   # 更新 Figure 物件的布
    # 回傳 a頁面                         # 這個是圖像介面
    return render_template ("a.html" ) + fig.to_html(include_plotlyjs='cdn')

# 點擊載入b功能頁面
@app.route("/b", methods=["GET"])
def b():
    return render_template("b.html")
# 點擊載入c功能頁面
@app.route("/c", methods=["GET"])
def c():
    return render_template("c.html")
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
app.run(port=3000)