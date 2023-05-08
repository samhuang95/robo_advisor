from pyecharts.charts import Bar, Line
from pyecharts import options as opts

class DrawChart:
  def bar(self, title, x_label, y_label, x, y):
    chart = Bar()
    chart.add_xaxis(x)
    chart.add_yaxis(y_label, y)
    chart.set_global_opts(
      title_opts=opts.TitleOpts(title=title),
      xaxis_opts=opts.AxisOpts(name=x_label),
      yaxis_opts=opts.AxisOpts(name=y_label)
    )
    chart_html = chart.render_embed()
    return chart_html
  
  def line(self, title, x_label, y_label, x, y):
    chart = Line()
    chart.add_xaxis(x)
    chart.add_yaxis(y_label, y)
    chart.set_global_opts(
      title_opts=opts.TitleOpts(title=title),
      xaxis_opts=opts.AxisOpts(name=x_label),
      yaxis_opts=opts.AxisOpts(name=y_label)
    )
    chart_html = chart.render_embed()
    return chart_html
