import numpy as np
import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import GRU, Dense
from tensorflow import keras
from keras.callbacks import EarlyStopping

# 讀取數據
dataItem = read_csv('./PD_adddate2.csv', usecols=[15], engine='python')

data = dataItem.values
data = data.astype('float32')
# 繪製原始數據
plt.figure(figsize=(14, 6))
print(data.shape)
plt.plot(data)
plt.show()

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
# early_stopping = EarlyStopping(monitor='loss', patience=50, verbose=1)
hist = model.fit(traindataNew, trainLabelNew, epochs=500, batch_size=32, verbose=1)
# hist = model.fit(traindataNew, trainLabelNew, epochs=500, batch_size=32, verbose=1, callbacks=[early_stopping])

# 繪製訓練損失
loss = hist.history["loss"]
epochs = range(len(loss))
plt.plot(epochs, loss, 'r-', label="Training loss")
plt.title('Training Loss')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

# 預測
trainPredict = model.predict(traindataNew)
testPredict = model.predict(testdataNew)
len(trainPredict)

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
plt.show()

# 預測未來3個月銷售額
future_days = 90
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
plt.show()

# 創建日期範圍
start_date = datetime.today()
date_range = [start_date + timedelta(days=x) for x in range(future_days)]

# 創建 DataFrame 並顯示
predictions_df = pd.DataFrame({'Date': date_range, 'Predicted Sales': np.squeeze(future_predictions)})
pd.set_option('display.max_rows', None)  # 顯示所有行
print(predictions_df)