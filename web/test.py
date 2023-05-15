# from datetime import datetime, timedelta   # 匯入 datetime 和 timedelta 模組
# import random   # 匯入 random 模組
# import plotly.graph_objs as go   # 匯入 plotly.graph_objs 模組並使用 go 簡寫
# from flask import Flask, request   # 匯入 Flask 和 request 模組

# app = Flask(__name__)   # 建立 Flask app 物件cl

# @app.route('/')   # 路由定義為根目錄
# def index():
#     return '''
#         <form action="/plot" method="get">
#             <label for="start_date">Start Date:</label>
#             <input type="date" id="start_date" name="start_date" value="2023-05-06">
#             <br>
#             <label for="end_date">End Date:</label>
#             <input type="date" id="end_date" name="end_date" value="2023-05-06">
#             <br><br>
#             <input type="submit" value="Plot">
#         </form>
#     '''
#     # 回傳一個 HTML 表單，該表單包含 Start Date 和 End Date 兩個日期欄位和一個提交按鈕

# @app.route('/plot', methods=['GET', 'POST'])   # 路由定義為 /plot，支援 GET 和 POST 方法
# def plot():
#     if request.method == 'POST':   # 如果是 POST 請求
#         start_date_str = request.form['start_date']   # 從 request.form 取得 start_date 參數
#         end_date_str = request.form['end_date']   # 從 request.form 取得 end_date 參數
#     else:   # 如果是 GET 請求
#         start_date_str = request.args.get('start_date')   # 從 request.args 取得 start_date 參數
#         end_date_str = request.args.get('end_date')   # 從 request.args 取得 end_date 參數
#     start_date = datetime.strptime(start_date_str, '%Y-%m-%d')   # 將 start_date_str 字串轉為 datetime 物件
#     end_date = datetime.strptime(end_date_str, '%Y-%m-%d')   # 將 end_date_str 字串轉為 datetime 物件
#     delta = end_date - start_date   # 計算日期區間
#     x = [start_date + timedelta(days=i) for i in range(delta.days + 1)]   # 產生日期區間內每一天的日期
#     y = [random.randint(0, 100) for _ in range(delta.days + 1)]   # 產生一個數值列表，該列表長度與日期區間相同
#     fig = go.Figure()   # 建立一個 plotly 的 Figure 物件
#     fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))   # 在 Figure 物件中添加一個 Scatter 圖形
#     fig.update_layout(title=f'Date Range: {start_date_str} - {end_date_str}', xaxis_title='Date', yaxis_title='Value')   # 更新 Figure 物件的布
#     date_picker_html = f'''
#         <form action="/plot" method="post">
#             <label for="start_date">Start Date:</label>
#             <input type="date" id="start_date" name="start_date" value="{start_date_str}">
#             <br>
#             <label for="end_date">End Date:</label>
#             <input type="date" id="end_date" name="end_date" value="{end_date_str}">
#             <br><br>
#             <input type="submit" value="Plot">
#         </form>
#     '''
#     return date_picker_html + fig.to_html(include_plotlyjs='cdn')

# if __name__ == '__main__':
#     app.run(debug=True)


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
# 取出所有key值
a_all = list(a.keys())

print(a_all)
