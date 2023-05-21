from pyecharts.charts import Bar, Line
from pyecharts import options as opts

class DrawChart:
  def bar(self, title, x_label, y_label1, y_label2, x, y, y2):
    chart = Bar()
    chart.add_xaxis(x)
    chart.add_yaxis(y_label1, y)
    chart.add_yaxis(y_label2, y2)
    yaxis_opts=[
    opts.AxisOpts(name=y_label1),
    opts.AxisOpts(name=y_label2)]
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=x_label),
    )
    chart_html = chart.render_embed()
    return chart_html
  
  def lines_times(self, title, x_label, y_label, x, y):
    chart = Line()

    for shop_name, sales in y.items():
        x_dates = [date.strftime("%Y-%m-%d") for date in x[shop_name]]
        chart.add_xaxis(x_dates)
        chart.add_yaxis(shop_name, sales)

    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(
            name=x_label,
            type_="time",
            axislabel_opts=opts.LabelOpts(),
        ),
        yaxis_opts=opts.AxisOpts(name=y_label),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )

    chart_html = chart.render_embed()
    return chart_html
  
  def lines7(self, title, x_label, y_label, x, y):
    chart = Line()
    chart.add_xaxis(x)

    for shop_name, sales in y.items():
        chart.add_yaxis(shop_name, sales)

    chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(name=x_label),
        yaxis_opts=opts.AxisOpts(name=y_label),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )

    chart_html = chart.render_embed()
    return chart_html

