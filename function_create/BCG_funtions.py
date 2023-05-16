import pandas as pd
import matplotlib.pyplot as plt
from functions.connect_to_db import SQLcommand
from datetime import datetime
import matplotlib.font_manager
import numpy as np
from math import floor


# 市場份額market_share：
def market_share():
    market_share_result = []
    plants_names = ['七變化虎耳草','西瓜皮椒草','大麻葉花燭','西瓜皮椒草','白斑合果芋','白斑姑婆芋','白斑龜背芋','明脈火鶴','油畫竹芋','紅玉椒草','姬龜背芋','斑葉心葉蔓綠絨','斑葉白鶴芋','斑葉豹紋竹芋','絨葉蔓綠絨','黑合果芋','黑頂卷柏','瑞士起司窗孔龜背芋','銅鏡觀音蓮','斑葉獨角獸蔓綠絨','飄帶火鶴','灑金蔓綠絨']
    for plants_name in plants_names:
        monthly_sale = SQLcommand().get(f'SELECT SUM(monthly_sales) FROM plants where plant_type = "{plants_name}";')[0][0]
        now = datetime.now()
        month = now.strftime("%m")
        year = now.strftime("%y")
        all_market_sale = SQLcommand().get(f'SELECT SUM(monthly_sales) FROM plants;')[0][0]
        if monthly_sale is not None and all_market_sale is not None:  
            msc = (float(monthly_sale) / float(all_market_sale)) * 100
        else:
            print(f"No sales data for plant {plants_name} in month {month}, year {year}")
            msc=0
        market_share_result.append(msc)
    return market_share_result

result = market_share()
print(result)

def growth_rate():
    growth_rate_result = []
    df = pd.read_csv('predictions_gold.csv')
    plants_names = ['七變化虎耳草','西瓜皮椒草','大麻葉花燭','西瓜皮椒草','白斑合果芋','白斑姑婆芋','白斑龜背芋','明脈火鶴','油畫竹芋','紅玉椒草','姬龜背芋','斑葉心葉蔓綠絨','斑葉白鶴芋','斑葉豹紋竹芋','絨葉蔓綠絨','黑合果芋','黑頂卷柏','瑞士起司窗孔龜背芋','銅鏡觀音蓮','斑葉獨角獸蔓綠絨','飄帶火鶴','灑金蔓綠絨']
    now = datetime.now()
    month = int(now.strftime("%m"))
    year = int(now.strftime("%Y"))
    for col, plants_name in zip(df.columns, plants_names):
        predict_value = df[col].iloc[-1]
#         print(predict_value)
        if month in [1, 2, 3]:
            season_total_sale = SQLcommand().get("SELECT SUM(sale_products) FROM product_detail WHERE MONTH(date_time) IN (4, 5, 6) AND YEAR(date_time) = {} AND product_name LIKE '%{}%'".format(year-1, plants_name))
        elif month in [4, 5, 6]:
            season_total_sale = SQLcommand().get("SELECT SUM(sale_products) FROM product_detail WHERE MONTH(date_time) IN (7, 8, 9) AND YEAR(date_time) = {} AND product_name LIKE '%{}%'".format(year-1, plants_name))
        elif month in [7, 8, 9]:
            season_total_sale = SQLcommand().get("SELECT SUM(sale_products) FROM product_detail WHERE MONTH(date_time) IN (10, 11, 12) AND YEAR(date_time) = {} AND product_name LIKE '%{}%'".format(year-1, plants_name))
        elif month in [10, 11, 12]:
            season_total_sale = SQLcommand().get("SELECT SUM(sale_products) FROM product_detail WHERE MONTH(date_time) IN (1, 2, 3) AND YEAR(date_time) = {} AND product_name LIKE '%{}%'".format(year, plants_name))
#         print(season_total_sale)
        if season_total_sale[0][0] is None:
            # season_total_sale = 10
            print(f"No sales data for plant {plants_name},predict value{predict_value}")
            # continue
            grc = 0
        else:
            season_total_sale = float(season_total_sale[0][0])
            grc = ((predict_value - season_total_sale) / season_total_sale) * 100 
        growth_rate_result.append(grc)      
    return growth_rate_result
result = growth_rate()
print(result)

# 熱銷 單一植物4月銷量 / 24種 整個市場4月銷量 
def hot_sales():
    hot_sales_status = []
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%y")
    plants_names = ['七變化虎耳草','西瓜皮椒草','大麻葉花燭','西瓜皮椒草','白斑合果芋','白斑姑婆芋','白斑龜背芋','明脈火鶴','油畫竹芋','紅玉椒草','姬龜背芋','斑葉心葉蔓綠絨','斑葉白鶴芋','斑葉豹紋竹芋','絨葉蔓綠絨','黑合果芋','黑頂卷柏','瑞士起司窗孔龜背芋','銅鏡觀音蓮','斑葉獨角獸蔓綠絨','飄帶火鶴','灑金蔓綠絨']
    for plants_name in plants_names:
        monthly_sales = SQLcommand().get(f'SELECT SUM(monthly_sales) FROM plants where plant_type = "{plants_name}";')[0][0]
        total_sale = SQLcommand().get(f'SELECT SUM(monthly_sales) FROM plants;')[0][0]
        if monthly_sales is not None and total_sale is not None and total_sale != 0:
            hsc = (float(monthly_sales) / float(total_sale)) * 1000
            print(hsc)
        if hsc > 70:
            sale_status = "熱銷"
        elif 30 <= hsc <= 70:
            sale_status = "正常"
        else:
            sale_status = "滯銷"
        hot_sales_status.append(sale_status)
    return  hot_sales_status
result = hot_sales()
print(result)


def call_functions():
    ms = market_share()
    gr = growth_rate()
    hs = hot_sales()
    return ms,gr,hs

# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
ms, gr, hs = call_functions()
plants_names = ['七變化虎耳草','西瓜皮椒草','大麻葉花燭','西瓜皮椒草','白斑合果芋','白斑姑婆芋','白斑龜背芋','明脈火鶴','油畫竹芋','紅玉椒草','姬龜背芋','斑葉心葉蔓綠絨','斑葉白鶴芋','斑葉豹紋竹芋','絨葉蔓綠絨','黑合果芋','黑頂卷柏','瑞士起司窗孔龜背芋','銅鏡觀音蓮','斑葉獨角獸蔓綠絨','飄帶火鶴','灑金蔓綠絨']
inventory = [200,1800,2000,3000,1200,420,500,280,2000,5000,220,5200,2700,2900,820,1111,5200,200,1790,6000,1000,2500]

data = []
for i in range(len(plants_names)):
    data_dict = {"name": plants_names[i], 
                 "market_share": ms[i], 
                 "growth_rate": gr[i], 
                 "inventory": inventory[i], 
                 "status": hs[i]}
    data.append(data_dict)

def draw_bcg_matrix(data):
    df = pd.DataFrame(data)
    # 過濾掉growth_rate=0的資料
    df = df[df["growth_rate"] != 0]

    color_mapping = {"熱銷": "red", "正常": "green", "滯銷": "blue"}
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df["market_share"], df["growth_rate"], s=df["inventory"], c=df["status"].map(color_mapping), alpha=0.5)

    for i, row in df.iterrows():
        # 產生隨機的微小偏移量
        dx, dy = np.random.uniform(-1, 1, 2)
        # 用偏移量調整標籤位置
        ax.annotate(row["name"], (row["market_share"] + dx, row["growth_rate"] + dy))


    # 設置X軸和Y軸標籤
    ax.set_xlabel("Market Share (%)")
    ax.set_ylabel("Growth Rate (%)")
    # 添加網格線和BCG矩陣象限劃分線
    ax.grid()
    growth_rates = growth_rate()  # get the growth rates
    growth_rates.sort()  # sort the list in place
    x = floor(len(growth_rates)*0.6)
    xx = growth_rates[x] - 0.1

    market_shares = market_share()
    market_shares.sort()
    y = floor(len(market_shares)*0.6)
    yy= market_shares[y] - 0.1

    ax.axhline(xx, color="black", linestyle="--")
    ax.axvline(yy, color="black", linestyle="--")

    xlims = ax.get_xlim()
    ylims = ax.get_ylim()

    # Question Mark 在左上象限
    ax.text((xlims[0] + yy) / 2, (ylims[1] + xx) / 2, "Question Mark", fontsize=12, ha="center", va="center", color='red')
    # Star 在右上象限
    ax.text((xlims[1] + yy) / 2, (ylims[1] + xx) / 2, "Star", fontsize=12, ha="center", va="center", color='red')
    # Dog 在左下象限
    ax.text((xlims[0] + yy) / 2, (ylims[0] + xx) / 2, "Dog", fontsize=12, ha="center", va="center", color='red')
    # Cash Cow 在右下象限
    ax.text((xlims[1] + yy) / 2, (ylims[0] + xx) / 2, "Cash Cow", fontsize=12, ha="center", va="center", color='red')

    # 顯示圖表
    plt.show()
    
result = draw_bcg_matrix(data)
print(result)