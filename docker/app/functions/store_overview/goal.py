from pyecharts.charts import Line
from pyecharts import options as opts
import csv
from datetime import date, datetime, timedelta
from flask import Flask, render_template
import sys
# sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from ..connect_to_db import SQLcommand

# 【kpi 數值】
def line_stack_area(time_select):
    # 【kpi 數值】
    time_select_dt = datetime.strptime(time_select, '%Y-%m-%d')
    month = time_select_dt.strftime("%m")
    year = time_select_dt.strftime("%Y")
    kpi_rowdata = SQLcommand().get(f'''
    SELECT date_time, predicted_sales FROM kpi_predicted
    WHERE MONTH(date_time) LIKE {month} AND YEAR(date_time) = {year};
    ''')
    # 轉成 dict
    kpi_data = {date: value for date, value in kpi_rowdata}   

    # 【當月銷售數值】
    month_sales_rowdata = SQLcommand().get(f'''
    SELECT date_time,SUM(total_sales) FROM product_detail
    WHERE MONTH(date_time) = {month} AND YEAR(date_time) = {year}
    GROUP BY date_time;
    ''')
    # 轉成 dict
    month_sales = {date: value for date, value in month_sales_rowdata}   

    line_kpi = Line(init_opts=opts.InitOpts(theme='light', width='100%', height='100%'))
    line_kpi.add_xaxis(list(kpi_data.keys()))
    line_kpi.add_yaxis('當月 KPI', list(kpi_data.values()),
                        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(123, 123, 123, 1)'),
                        linestyle_opts=opts.LineStyleOpts(color='rgba(123, 123, 123, 1)'),
                        label_opts=opts.LabelOpts(color='#D26900', font_size=30, position='right')
                        )

    line_sales = Line()
    line_sales.add_xaxis(list(month_sales.keys()))
    line_sales.add_yaxis('月銷量', list(month_sales.values()), 
                        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='rgba(210, 105, 0, 0.65)'),
                        linestyle_opts=opts.LineStyleOpts(color='rgba(210, 105, 0, 0.65)'),
                        label_opts=opts.LabelOpts(color='#585858', font_size=30, position='right')
                        )
    line_kpi.set_series_opts(label_opts=opts.LabelOpts(color='rgba(123, 123, 123, 1)'))
    line_sales.set_series_opts(label_opts=opts.LabelOpts(color='rgba(210, 105, 0, 0.65)'))  


    
    # 使用 line_stack_area 函式並傳入月銷量數據
    line_chart = line_kpi.overlap(line_sales)
    
    # 設定圖表的其他選項
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title=f"{month} 月KPI 達成率 "), 
                               xaxis_opts=opts.AxisOpts(name="日期"),
                               yaxis_opts=opts.AxisOpts(name="銷售金額"))

    return line_chart

# 使用 line_stack_area 函式並傳入月銷量數據
line_chart = line_stack_area('2023-05-11')

# 顯示圖表
line_chart.render("line_chart.html")