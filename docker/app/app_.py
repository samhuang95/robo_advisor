from flask import Flask, render_template, request
from functions.image_predict import predict_image
# from functions.connect_to_db import SQLcommand
# from functions.draw_chart import DrawChart
# from datetime import datetime

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('e.html')
  
  scores = []
  files = request.files.getlist('file')
  for file in files:
    file.save('static/photos/' + file.filename)
    evaluate = predict_image(f'static/photos/{file.filename}')
    scores.append({'圖片名稱': file.filename, '圖片評價': evaluate})
  return render_template('e.html', scores=scores)

if __name__ == '__main__':
  app.run(host='0.0.0.0')
