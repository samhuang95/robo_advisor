from flask import Flask, render_template
import plotly.graph_objs as go
import plotly.offline as opy

app = Flask(__name__)

@app.route('/')
def index():
    # 创建Plotly图表
    trace = go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3])
    data = [trace]
    layout = go.Layout(title='預測')
    fig = go.Figure(data=data, layout=layout)

    # 将图表转换为HTML文件
    div = opy.plot(fig, auto_open=False, output_type='div')

    # 渲染模板并将图表发送到客户端
    return render_template('test.html', div_placeholder=div)

if __name__ == '__main__':
    app.run(port=4000)
