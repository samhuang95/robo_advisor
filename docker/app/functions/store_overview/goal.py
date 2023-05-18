from pyecharts.charts import Line
from pyecharts import options as opts
import csv
from datetime import date, datetime, timedelta

now = datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")

with open(f'./train_data/{year}{month}_train_result.csv', newline='') as csvfile:
    # 以 DictReader 讀取 CSV 檔案
    reader = csv.DictReader(csvfile)
    # 以 dictionary 儲存資料
    data_dict = {}
    for row in reader:
        # 將每一筆資料轉換成 dictionary
        name = row['name']
        age = row['age']
        data_dict[name] = age




def line_stack_area(month_kpi, month_sales):
    line_kpi = Line()
    line_kpi.add_xaxis(list(month_kpi.keys()))
    line_kpi.add_yaxis('當月 KPI', list(month_kpi.values()), areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(62, 197, 197, 1)'))

    line_sales = Line()
    line_sales.add_xaxis(list(month_sales.keys()))
    line_sales.add_yaxis('月銷量', list(month_sales.values()), areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(246, 221, 0, 0.65)'))

    line_chart = line_kpi.overlap(line_sales)
    return line_chart

month_kpi = {
    '2023-01-01': 100,
    '2023-01-02': 190,
    '2023-01-03': 240,
    '2023-01-04': 530,
    '2023-01-05': 90,
    # ... 其他日期和對應的銷量數據
}

month_sales = {
    '2023-01-01': 200,
    '2023-01-02': 200,
    '2023-01-03': 230,
    # ... 其他日期和對應的銷量數據
}

# 使用 line_stack_area 函式並傳入月銷量數據
line_chart = line_stack_area(month_kpi, month_sales)

# 設定圖表的其他選項
line_chart.set_global_opts(title_opts=opts.TitleOpts(title="堆疊區域圖"), 
                           xaxis_opts=opts.AxisOpts(name="日期"),
                           yaxis_opts=opts.AxisOpts(name="數量"))

# 顯示圖表
line_chart.render("line_chart.html")