from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import math



class DrawChart:
  def bar(self, title, x_label, y_label1, y_label2, x, y, y2):
    chart = Bar()
    chart.add_xaxis(x)
    chart.add_yaxis(y_label1, y, color="#FD9A32")
    chart.add_yaxis(y_label2, y2, color="#666666")
    yaxis_opts=[
    opts.AxisOpts(name=y_label1),
    opts.AxisOpts(name=y_label2)]
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=x_label),
    )
    chart_html = chart.render_embed()
    return chart_html
  

# rating & messages
  def lines_times(self, title, x_label, y_label, x, y):
    chart = Line()

    fix_color={'麗都花園':"#FFD306",
               "珍奇植物":"#A8FF24",
               "開心農元":"#AFAF61",
               "糀町植葉":"#FF8040",
               "沐時園藝":"#B766AD",
               "小李植栽":"#9999CC",
               "南犬植栽":"#6FB7B7",
               "宅栽工作室":"#FF359A",
    }

    for i, (shop_name, sales) in enumerate(y.items()):
        x_dates = [date.strftime("%Y-%m-%d") for date in x[shop_name]]
        chart.add_xaxis(x_dates)
        chart.add_yaxis(
            shop_name,
            sales,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color=fix_color[shop_name]),  # 根據索引選取顏色
        )

    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(
            name=x_label,
            type_="time",
            axislabel_opts=opts.LabelOpts(formatter=JsCode("function (value) { return echarts.format.formatTime('yyyy-MM-dd', value); }")),
),
        yaxis_opts=opts.AxisOpts(name=y_label),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )

    chart_html = chart.render_embed()
    return chart_html
  
  # daily_sales
  
  def lines7(self, title, x_label, y_label, x, y):
    chart = Line()
    chart.add_xaxis(x)

    fix_color={'麗都花園':"#FFD306",
               "珍奇植物":"#A8FF24",
               "開心農元":"#AFAF61",
               "糀町植葉":"#FF8040",
               "沐時園藝":"#B766AD",
               "小李植栽":"#9999CC",
               "南犬植栽":"#6FB7B7",
               "宅栽工作室":"#FF359A",
    }

    for shop_name, sales in y.items():
        chart.add_yaxis(
            shop_name,
            sales,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(color=fix_color[shop_name]),  # Use the specified color
        )

    max_value = int(max(max(sales) for sales in y.values()))  # Get the maximum value
    min_value = int(min(min(sales) for sales in y.values()))  # Get the minimum value

    num_intervals = 5  # Number of intervals for y-axis ticks

    # Calculate y-axis tick range
    max_tick = math.ceil(max_value / 1000) * 1000
    min_tick = math.floor(min_value / 1000) * 1000

    # Calculate tick interval
    interval = (max_tick - min_tick) / (num_intervals - 1)

    # Set y-axis tick options
    y_axis_opts = opts.AxisOpts(
    name=y_label,
    type_="value",
    axislabel_opts=opts.LabelOpts(formatter=JsCode("function (value) { return value.toLocaleString('en'); }")),
    splitline_opts=opts.SplitLineOpts(is_show=False),
    min_=min_tick,
    max_=max_tick,
    interval=interval,
)


    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=x_label),
        yaxis_opts=y_axis_opts,
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )

    chart_html = chart.render_embed()
    return chart_html

