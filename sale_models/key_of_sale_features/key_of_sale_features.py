#Your Guide to Linear Regression Models(https://www.kdnuggets.com/2020/10/guide-linear-regression-models.html)
#Linear Regression in Python(https://medium.com/@harishreddyp98/linear-regression-in-python-c164149b93ab)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from sklearn.metrics import r2_score
import statsmodels.api as sm


print('\n=======< load data >=======')
df = pd.read_csv('./product_overview_20210401-20230409.csv', sep=',')
print(df.head())

sns.pairplot(df)
# 使用 seaborn 套件中的 pairplot 函式，繪製出兩兩欄位之間的關聯性
# plt.show()
plt.savefig('sns_pairplot.png')
plt.close()

mask = np.tril(df.corr())
# df.corr() = correlation，將 df 中的數值，轉為變數與變數之間的相關係數
# 使用numpy 套件中的 tril 函式，將矩陣圖中的下三角的數值，全部轉為 0，
# 因為下三角與上三角的資訊是對稱一樣的
sns.heatmap(df.corr(), fmt='.1g', annot=True, cmap= 'cool', mask=mask)
# 使用 seaborn 套件中的 heatmap 函式，繪製熱力圖
# fmt 參數為 .1g，表示以浮點數的格式顯示相關係數，精確度保留一位小數
# annot 參數為 True，表示在熱力圖上標註出相關係數的數值
# cmap 參數為 cool，表示使用 cool 顏色地圖作為熱力圖的顏色
# mask 參數為 mask 變數，表示遮蔽掉矩陣的下三角部分
# plt.show()
plt.savefig('sns_heatmap.png')
plt.close()

print('\n=======< adjust dataframe >=======')
X = df.drop(['total_sales'], axis=1)
Y = df['total_sales']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
print(X_train.shape,Y_train.shape,X_test.shape,Y_test.shape)
# 呈現出訓練及與測試集的資料數量、欄位數量

print('\n=======< model.training >=======')
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
X_train_poly_df = pd.DataFrame(X_train_poly, columns=poly.get_feature_names(X_train.columns))

print(X_train_poly.shape)
print(X_test_poly.shape)

# 使用新的資料集進行模型訓練和預測
model = LinearRegression()
model.fit(X_train_poly, Y_train)
y_pred = model.predict(X_test_poly)

print(model.intercept_)
# .intercept_ 指線性回歸模型的截距，當自變數全部為 0 時，預測因變數創造的截距值
# 截距值通常用來校正模型的預測，當有新的自變數輸入模型時，
# 截距和每個自變數的權重都會對輸出值做出貢獻

# 通常使用截距和斜率來描述線性關係
# 線性關係指的是兩個變數之間存在著直線關係，
# 當其中一個變數的值發生改變時，另一個變數的值也會隨之按照固定比例發生變化
# 舉例：如果學習時間和成績之間存在著直線關係，
# 那麼當學生增加學習時間時，他的成績也會隨之按照某個比例增加。

# 自變數(independent variable) = 影響因素，
# 舉例：在研究中被研究者所控制或調整的變數，
# 通常是研究者可以自行控制或改變的變數，
# 它的變化對於因變數（反應變數）的變化有所影響

print('\n=======< coeff_df of each column >=======')
coeff_df = pd.DataFrame(model.coef_, X_train_poly_df.columns, columns =['Coefficient'])
print(coeff_df)

print('\n=======< model training score >=======')
#驗証模型
y_pred = model.predict(X_test_poly)

print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(Y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, y_pred)))
print('R Squared Score is:', r2_score(Y_test, y_pred))  # higher R² indicates a better fit for the model

# #interpret and improve
# #X2 = sm.add_constant(X_train)
# #model_stats = sm.OLS(Y_train.values.reshape(-1,1), X2).fit()
# #print(model_stats.summary())
# print('\n=======< setting advertise and estimate final incomes >=======')
# # 假設今天投放 
# # 50 元的預算在 TV 廣告
# # 30 元的預算在 radio 廣告
# # 10 元的預算在 Newspaper 廣告
# # 預測會有多少收益
# example = [50, 30, 10]  
# output = model.intercept_ + sum(example*model.coef_)
# print(f"Estimate Sales:{output}")

# example = [30, 50, 10]  
# output = model.intercept_ + sum(example*model.coef_)
# print(f"Estimate Sales:{output}")

# example = [20, 50, 20]  
# output = model.intercept_ + sum(example*model.coef_)
# print(f"Estimate Sales:{output}")