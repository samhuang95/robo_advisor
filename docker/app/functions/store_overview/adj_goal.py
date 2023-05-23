from pyecharts.charts import Line
from pyecharts import options as opts
import csv
from datetime import date, datetime, timedelta
from flask import Flask, render_template
import sys
sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from connect_to_db import SQLcommand


now = datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")


# app = Flask(__name__)

# def line_stack_area(kpi_data, month_sales):
#     line_kpi = Line(init_opts=opts.InitOpts(theme='light', width='1000px', height='600px'))
#     line_kpi.add_xaxis(list(kpi_data.keys()))
#     line_kpi.add_yaxis('當月 KPI', list(kpi_data.values()), 
#                        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(62, 197, 197, 1)'),
#                        linestyle_opts=opts.LineStyleOpts(color='blue'))

#     line_sales = Line()
#     line_sales.add_xaxis(list(month_sales.keys()))
#     line_sales.add_yaxis('月銷量', list(month_sales.values()), 
#                          areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(225, 0, 0, 0.65)'),
#                          linestyle_opts=opts.LineStyleOpts(color='red'),
#                          label_opts=opts.LabelOpts(color='red', font_size=12)
#                          )

#     line_chart = line_kpi.overlap(line_sales)
    
#     line_chart.set_global_opts(title_opts=opts.TitleOpts(title=f"{month} 月KPI 達成率 "), 
#                                xaxis_opts=opts.AxisOpts(name="日期"),
#                                yaxis_opts=opts.AxisOpts(name="銷售金額"))

#     return line_chart

# @app.route('/')
# def index():
#     # 【kpi 數值】
#     with open(f'./train_data/{year}{month}_train_result.csv', newline='') as csvfile:
#         # 以 DictReader 讀取 CSV 檔案
#         reader = csv.DictReader(csvfile)
#         # 以 dictionary 儲存資料
#         pred_dict = {}
#         for row in reader:
#             # 將每一筆資料轉換成 dictionary
#             Date = row['Date']
#             Predicted_Sales = round(float(row['Predicted_Sales']))
#             pred_dict[Date] = Predicted_Sales

#     month = int(yesterday.strftime("%m"))
#     kpi_data = {}
#     for date, value in pred_dict.items():
#         if date.startswith(f'{year}/{month}'):
#             kpi_data[date] = value
#     # -------------------------------------------------------------
#     # 【當月銷售數值】

    



#     month = yesterday.strftime("%m")
#     with open(f'./dataset/all_data{year}-{month}-{day}.csv', newline='',encoding = 'utf-8') as csvfile:
#         # 以 DictReader 讀取 CSV 檔案
#         reader = csv.DictReader(csvfile)
#         # 以 dictionary 儲存資料
#         month_dict = {}
#         for row in reader:
#             # 將每一筆資料轉換成 dictionary
#             Date = row['date']
#             daily_sales = round(float(row['daily_sales']))
#             month_dict[Date] = daily_sales

#     sale_dict = {}
#     for key, value in month_dict.items():
#         modified_key = key.replace('-', '/').replace('-0', '-').replace('/0', '/')
#         sale_dict[modified_key] = value

#     month = int(yesterday.strftime("%m"))
#     month_sales = {}
#     for date, value in sale_dict.items():
#         if date.startswith(f'{year}/{month}'):
#             month_sales[date] = value

#     line_chart = line_stack_area(kpi_data, month_sales)
#     chart_options = line_chart.dump_options()
#     return render_template('index.html', chart_options=chart_options)

# if __name__ == '__main__':
#     app.run(debug=True)





# -------------------------------------------------------------
# 【kpi 數值】
with open(f'./train_data/{year}{month}_train_result.csv', newline='') as csvfile:
    # 以 DictReader 讀取 CSV 檔案
    reader = csv.DictReader(csvfile)
    # 以 dictionary 儲存資料
    pred_dict = {}
    for row in reader:
        # 將每一筆資料轉換成 dictionary
        Date = row['Date']
        Predicted_Sales = round(float(row['Predicted_Sales']))
        pred_dict[Date] = Predicted_Sales

month = int(yesterday.strftime("%m"))
kpi_data = {}
for date, value in pred_dict.items():
    if date.startswith(f'{year}/{month}'):
        kpi_data[date] = value
# -------------------------------------------------------------
# 【當月銷售數值】
month = yesterday.strftime("%m")
with open(f'./dataset/all_data{year}-{month}-{day}.csv', newline='',encoding = 'utf-8') as csvfile:
    # 以 DictReader 讀取 CSV 檔案
    reader = csv.DictReader(csvfile)
    # 以 dictionary 儲存資料
    month_dict = {}
    for row in reader:
        # 將每一筆資料轉換成 dictionary
        Date = row['date']
        daily_sales = round(float(row['daily_sales']))
        month_dict[Date] = daily_sales

sale_dict = {}
for key, value in month_dict.items():
    modified_key = key.replace('-', '/').replace('-0', '-').replace('/0', '/')
    sale_dict[modified_key] = value

month = int(yesterday.strftime("%m"))
month_sales = {}
for date, value in sale_dict.items():
    if date.startswith(f'{year}/{month}'):
        month_sales[date] = value


# -------------------------------------------------------------
def line_stack_area(kpi_data, month_sales):
    line_kpi = Line(init_opts=opts.InitOpts(theme='light', width='1000px', height='600px'))
    line_kpi.add_xaxis(list(kpi_data.keys()))
    line_kpi.add_yaxis('當月 KPI', list(kpi_data.values()), 
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(62, 197, 197, 1)'),
                       linestyle_opts=opts.LineStyleOpts(color='rgba(62, 197, 197, 1)'))


    line_sales = Line()
    line_sales.add_xaxis(list(month_sales.keys()))
    line_sales.add_yaxis('月銷量', list(month_sales.values()), 
                         areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(225, 0, 0, 0.65)'),
                         linestyle_opts=opts.LineStyleOpts(color='rgba(225, 0, 0, 0.65)'),
                         label_opts=opts.LabelOpts(color='yellow', font_size=30, position='right')
                         )
    line_kpi.set_series_opts(label_opts=opts.LabelOpts(color='blue'))
    line_sales.set_series_opts(label_opts=opts.LabelOpts(color='red'))  


    
    # 使用 line_stack_area 函式並傳入月銷量數據
    line_chart = line_kpi.overlap(line_sales)
    
    # 設定圖表的其他選項
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title=f"{month} 月KPI 達成率 "), 
                               xaxis_opts=opts.AxisOpts(name="日期"),
                               yaxis_opts=opts.AxisOpts(name="銷售金額"))

    return line_chart

# 使用 line_stack_area 函式並傳入月銷量數據
line_chart = line_stack_area(kpi_data, month_sales)

# 顯示圖表
line_chart.render("line_chart.html")

