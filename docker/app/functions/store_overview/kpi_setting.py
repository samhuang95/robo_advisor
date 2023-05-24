import numpy as np
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import GRU, Dense
from tensorflow import keras
from keras.callbacks import EarlyStopping
from sklearn.tree import DecisionTreeRegressor
import csv
from datetime import date, datetime, timedelta
import configparser
import sys
sys.path.append("..")  # 添加上一層資料夾至模組搜尋路徑
from connect_to_db import SQLcommand

# -----------------------------------------------------
# 每個月執行一次，計算出
# 匯出只有金額的訓練資料

df = SQLcommand().get('''
SELECT SUM(total_sales) AS total_sales
FROM product_detail
GROUP BY date_time
ORDER BY date_time;
''')

df = pd.DataFrame(df, columns=['total_sales'])


# data_list = list(df['date_time'])
# print(data_list)
# df = pd.DataFrame(data_list, columns=['total_sales'])
data = df.values
data = data.astype('float32')
# print(data)

# 繪製原始數據
plt.figure(figsize=(14, 6))
print(data.shape)
plt.plot(data)
now = datetime.now()
month = now.strftime("%m")
year = now.strftime("%Y")
# plt.show()
plt.savefig(f'/app/functions/store_overview/model_result/{year}{month}_origin_data.png')
plt.close()

# 數據預處理
def GetDataAndLabel(data, TimeStep):
    trainData, trainLabel = [], []
    for i in range(len(data)-TimeStep):
        TrainDataOne = data[i:(i+TimeStep), 0]
        trainData.append(TrainDataOne)
        trainLabel.append(data[i+TimeStep, 0])
    return np.array(trainData), np.array(trainLabel)

# 歸一化
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data)

# 切分訓練集和測試集
TrainDataNum = int(len(data) * 0.8)
TestDataNum = len(data) - TrainDataNum
trainData = data[0:TrainDataNum, :]
testData = data[TrainDataNum:len(data), :]
# 數據標籤
TimeStep = 14
traindataNew, trainLabelNew = GetDataAndLabel(trainData, TimeStep)
testdataNew, testLabelNew = GetDataAndLabel(testData, TimeStep)
print("traindataNew.shape :",traindataNew.shape)
print("trainLabelNew.shape :",trainLabelNew.shape)
print("testdataNew.shape :",testdataNew.shape)
print("testLabelNew.shape :",testLabelNew.shape)

# 改變維度
traindataNew = np.reshape(traindataNew, (traindataNew.shape[0], traindataNew.shape[1], 1))
testdataNew = np.reshape(testdataNew, (testdataNew.shape[0], testdataNew.shape[1], 1))
print("traindataNew.shape :",traindataNew.shape)
print("testdataNew.shape :",testdataNew.shape)

# 建立模型
model = keras.Sequential()
model.add(GRU(256, input_shape=(TimeStep, 1), return_sequences=True))
model.add(GRU(128, input_shape=(TimeStep, 1), return_sequences=True))
model.add(GRU(64, input_shape=(TimeStep, 1)))
model.add(Dense(1))
print(model.summary())

# 編譯和訓練模型
optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='mean_squared_error', optimizer=optimizer)
hist = model.fit(traindataNew, trainLabelNew, epochs=500, batch_size=64, verbose=1)
# early_stopping = EarlyStopping(monitor='loss', patience=50, verbose=1)
# hist = model.fit(traindataNew, trainLabelNew, epochs=500, batch_size=32, verbose=1, callbacks=[early_stopping])

# 繪製訓練損失
loss = hist.history["loss"]
epochs = range(len(loss))
plt.plot(epochs, loss, 'r-', label="Training loss")
plt.title('Training Loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
# plt.show()
plt.savefig(f'/app/functions/store_overview/model_result/{year}{month}_loss_data.png')
plt.close()


# 預測
trainPredict = model.predict(traindataNew)
testPredict = model.predict(testdataNew)
# len(trainPredict)

# 逆歸一化
trainRealPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainLabelNew])
testRealPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testLabelNew])
# 繪製預測結果
PredtrainingData = np.empty_like(data)
PredtestData = np.empty_like(data)
originaldata = scaler.inverse_transform(data)
PredtrainingData[:, :] = np.nan
PredtestData[:, :] = np.nan

PredtrainingData[TimeStep: len(trainPredict) + TimeStep, :] = trainRealPredict
PredtestData[len(trainPredict) + (TimeStep * 2) - 1: len(data) - 1, :] = testRealPredict

plt.figure(figsize=(14, 6))
plt.plot(originaldata, color='green', label="Original data")
plt.plot(PredtrainingData, color='red', label="Train data Predict")
plt.plot(PredtestData, color='blue', label="Test data Predict")
plt.legend()
# plt.show()
plt.savefig(f'/app/functions/store_overview/model_result/{year}{month}_ori_and_pred_data.png')
plt.close()

# 預測未來"幾天"月銷售額
future_days = 80
input_data = data[-TimeStep:]
input_data = np.reshape(input_data, (1, TimeStep, 1))

future_predictions = []
for i in range(future_days):
    prediction = model.predict(input_data)
    future_predictions.append(prediction[0])
    input_data = np.concatenate((input_data[:, 1:, :], prediction.reshape(1, 1, 1)), axis=1)

future_predictions = scaler.inverse_transform(future_predictions)

import pandas as pd
from datetime import datetime, timedelta

# 繪製未來預測結果
plt.figure(figsize=(14, 6))
plt.plot(range(future_days), future_predictions, color='blue', label="Future predictions")
plt.xlabel("Days")
plt.ylabel("Sales")
plt.legend()
# plt.show()
plt.savefig(f'/app/functions/store_overview/model_result/{year}{month}_predicted_data.png')
plt.close()

# 創建日期範圍
start_date = datetime.today()
date_range = [(start_date + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(future_days)]
# 創建 DataFrame 並顯示
predictions_df = pd.DataFrame({'Date': date_range, 'Predicted_Sales': np.squeeze(future_predictions)})

pd.set_option('display.max_rows', None)  # 顯示所有行

print(predictions_df)

mysql_column_names = '''(date_time, predicted_sales)'''

csv_column_names = ['Date', 'Predicted_Sales']

for i in range(len(predictions_df['Date'])):
    data_tuple = []
    for csv_column_name in csv_column_names:
        data_tuple.append(predictions_df[csv_column_name][i])
    values_tuple = tuple(data_tuple)
    
    SQLcommand().modify(f'''
    REPLACE INTO kpi_predicted 
        {mysql_column_names}
        VALUES {values_tuple}''')
    data_tuple = []
