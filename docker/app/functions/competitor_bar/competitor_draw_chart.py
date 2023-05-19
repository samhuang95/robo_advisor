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

