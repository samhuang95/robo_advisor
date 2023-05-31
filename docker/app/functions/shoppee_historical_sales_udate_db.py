import requests, os
import json
import pandas as pd
import time
import re
import random
import zlib
from selenium import webdriver
from seleniumwire import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime



from connect_to_db import SQLcommand

page=[4, 10, 8, 3, 3, 3, 1, 5]
href=['dicsp','mat1990m','a219787','paz.pan','sunshine.plant.art','yab7829','raising_trees','flychenjack01']
keyword = ['麗都Lido Garden花園農場',"珍奇植物 CarnivoRUs","開心農元 Nursery & Garden Center","糀町💮植葉栽花種介","Mushi 沐時園藝","小李植栽 - 觀葉植物專賣店 - 種好種滿享生活","🔰南犬🔰植栽_觀葉｜雨林｜家居擺飾｜","宅栽"]
date = datetime.now().date()


#建立 Chrome WebDriver 服務
# service = ChromeService(executable_path=ChromeDriverManager().install())
# service = ChromeService(executable_path='./chromedriver.exe')


#設定Chrome選項-啟動headless模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# 添加自定义请求头
options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"')
options.add_argument('--af-ac-enc-dat=AAcyLjQuMS0yAAABhEYD7joAAAjHAcEAAAAAAAAAAOYyhFB7rjob26/8rq6jA0F3J6Kfg5aGEX+GYncix7fIyPghAefe3JS894jq/3nC9cJjpEn32HTqasIUhFkInWzoCOj1uSC5kl6LU06aSrm61kX/Ny1L5jzxFjDrS1IzPHwt9muZUbatRPTf42k24UXHBZsir4fwWxQLVKw5gDu5CyybpSVWFCd7OLsY30Hj1OjSKZvDNTpkAhYqvdOyLCTGr41kHyFGV3ZaoQ01NX1u6R9AnBG6X9s1ynZK6vnTBgzBIOKTNFS4j1VT8sOl1BEtObri8ZUW3OTOHeCO4vGDCq4gRJFmvwSm1BNdccjxAekgEx3xwroP6ZL6LO5bh9QSxuKGYkUmR84CcHLB6dmMPnXDUGkagca9MFiK8RmRsrN2vcLDNTpkAhYqvdOyLCTGr41kKUmjTinalW5/ctjHa7Lte+06J5ekdC078Iv4wrMjrvbzUjYNqi2Hdu8tLPGrNL/jmEfixe8rpESf8+9J+WOK8kusILDBjMDq/xa+8hI9GWbdxIdVmB5payUD+EtCC4BUkWOzjLDykZY2dhCO2aemlpFjs4yw8pGWNnYQjtmnppZDbeO6witi5K5LrYrVnhWzWCX7lKDZYje5tgIJeETgYw=="')
options.add_argument('--accept="application/json"')
options.add_argument('--content-type="application/json"')
options.add_argument('--x-api-source="pc"')
options.add_argument('--x-requested-with="XMLHttpRequest"')
options.add_argument('--x-csrftoken="IDq3287GJnXS5JJj5c2p5NfuvByGNpst"')
options.add_argument('--sz-token="Ra/NJSFhMbpYXlWXB/kMKw==|tbtAeRuQraLaHXP0PPLER62V4RREUxTHlM0sHpOnYMwbMMQeM9+qLgkomlUGpUVkjby5btMmGHCl9DFdTYOavUNJ3LuXv0sobg==|oZGZsgOMDe5oaMrE|06|3"')
options.add_argument('--sec-ch-ua-platform="Windows"')
options.add_argument('--sec-fetch-site="same-origin"')
options.add_argument('--sec-fetch-mode="navigate"')
options.add_argument('--sec-fetch-dest="document"')
options.add_argument('--cookie="SPC_F=0RCpmsHgvQV42k0NLHTjOrfzTBdBM9Rz; REC_T_ID=2179080b-ca4f-11ed-8343-f4ee0822848e; _gcl_au=1.1.2075392250.1679667675; _fbp=fb.1.1679667676117.421908566; _clck=ttmnco|1|faj|0; SPC_CLIENTID=MFJDcG1zSGd2UVY0gkoqlnytpwtysjbq; SC_DFP=MPlNvYPNerLhCdFZKbHDPvwfboZFUsJr; SPC_U=981340189; SPC_R_T_IV=WVpIQWR5NjA5NFRMRVFtMg==; SPC_T_ID=sBisq8u3H3oOjlmc8QV3p3uFUvy7rgQm+k5PpbFW1pfWSk/lXTzssnLxSkGsl2kWf080G8cDAGwLtqk5YQpTlHA/56AXoy8CbQUamnRvOUy/ItxYr6jlVDPuMqTvaBNli3sjIm2x19/CnlrDAYz0t5EOPDzeKdopWi3G9kuFrq0=; SPC_T_IV=WVpIQWR5NjA5NFRMRVFtMg==; SPC_R_T_ID=sBisq8u3H3oOjlmc8QV3p3uFUvy7rgQm+k5PpbFW1pfWSk/lXTzssnLxSkGsl2kWf080G8cDAGwLtqk5YQpTlHA/56AXoy8CbQUamnRvOUy/ItxYr6jlVDPuMqTvaBNli3sjIm2x19/CnlrDAYz0t5EOPDzeKdopWi3G9kuFrq0=; _gac_UA-61915057-6=1.1684340307.CjwKCAjw9pGjBhB-EiwAa5jl3A-qj3ACjIXzNkgQrYynoYwKyOFCQs3JFE_7XOrAEgJhGY1qDLOEUxoCKWIQAvD_BwE; _ga_E4FV1WFT0L=GS1.1.1684341086.1.0.1684341086.60.0.0; __LOCALE__null=TW; csrftoken=KksKp07u1QgQfza3FQSZi2ABAKD1KrLl; _gcl_aw=GCL.1684582930.CjwKCAjw36GjBhAkEiwAKwIWyQfganqZ8TN5NwFZlVquo6SWR98URb1xylvGI2ssCpp5ebxWclXDIRoC4psQAvD_BwE; _med=refer; SPC_SI=tTljZAAAAAA1MGlkZnFHTsR09gAAAAAASnZJbm1QZGQ=; _gid=GA1.2.1754535228.1684678731; _QPWSDCXHZQA=9f4966ff-a767-4825-90fb-a6f1c079b422; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.1384401067.1679667680; shopee_webUnique_ccd=YmJ30d%2FZsShTSG55dRsLHQ%3D%3D%7ClL3oTmiH8sUMezpqU%2B8KmAfGPTFoXMzoSmx3IsorjEhmChcnSuywAEwXTfQoqAyqjGwMHJKHtr3SxsS%2BumFPzlocCHLgVZzJNyc%3D%7ClXi%2F7iUFOmZazVnO%7C06%7C3; ds=c164855a3a86821d6452d02b836cbcc3; _ga_RPSBE3TQZZ=GS1.1.1684850013.119.0.1684850412.60.0.0"')
options.add_argument('--if-none-match-="30360-LwHHHN5ro7vVG5KitkSL2tdY0rA"')


#建立Chrome Webdriver
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',chrome_options=options)
# driver = webdriver.Chrome(chrome_options=options)
time.sleep(random.randint(20, 30))

# # #商品數、粉絲數、評價數量
product_count=[]
fans_count =[]
rating_count =[]

# #搜尋目標賣場
for i in range(len(keyword)):
    # driver.get('https://shopee.tw/search?keyword='+keyword[i])
    driver.get(f'https://shopee.tw/{href[i]}')
    time.sleep(random.randint(70, 80))

    # #取得href
    # time.sleep(random.randint(70, 80))
    # hreff = driver.find_element(By.CLASS_NAME, 'shopee-search-user-item__username')
    # href.append(hreff.text)
    # time.sleep(random.randint(70, 80))
    
    # #點進目標賣場
    # driver.find_element(By.CSS_SELECTOR, '#main > div > div.dYFPlI > div > div > div.sdzgsX > div.shopee-search-user-brief > div > div.shopee-header-section__content > div > a.shopee-search-user-item__shop-info > div.shopee-search-user-item__nickname').click()
    # time.sleep(random.randint(70, 80))

    # #取得page總頁數
    # pagee=driver.find_element(By.CLASS_NAME, 'shopee-mini-page-controller__total').text
    # page.append(int(pagee))
    
    # 取得粉絲數
    g_fans_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(2) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text
    if "萬" in g_fans_count:
        g_fans_count=int(float(g_fans_count.replace('萬',"").replace(',', ''))*10000)
        fans_count.append(g_fans_count)
    else:
        fans_count.append(int(g_fans_count.replace(',', '')))

    # 取得商品數
    g_product_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(1) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text
    product_count.append(g_product_count)

    # 取得評價(數量)
    g_rating_count = driver.find_element(by=By.CSS_SELECTOR, value="#main > div > div:nth-child(3) > div > div > div > div.shop-page > div > div.shop-page__info > div > div.section-seller-overview-horizontal__seller-info-list > div:nth-child(4) > div.section-seller-overview__item-text > div.section-seller-overview__item-text-value").text.replace('(', '').replace(')', '').split(' ')[1]
    if "萬" in g_rating_count:
        g_rating_count=int(float(g_rating_count.split('個評價')[0].replace('萬',"").replace(',', ''))*10000)
        rating_count.append(g_rating_count)
    else:
        rating_count.append(int(g_rating_count.split('個評價')[0].replace(',', '')))


for p in range(len(product_count)):
    values = (str(date), keyword[p], fans_count[p], product_count[p], rating_count[p])
    sql = 'INSERT INTO offical_data (date, shop_name, fans_count, products_count, rating_counts) VALUES (%s, %s, %s, %s, %s)'
    try:
        SQLcommand().modify_tuple(sql, values)
    except Exception as e:
        print(f"發生異常:keyword[p]{e}")
print(f'已於{date}完成競品賣場的資料更新！','競品總數量' + str(len(keyword)))
    
        
SQLcommand().modify("""
    UPDATE offical_data
    SET shop_name = CASE
        WHEN shop_name = '開心農元 Nursery & Garden Center' THEN '開心農元'
        WHEN shop_name = '小李植栽 - 觀葉植物專賣店 - 種好種滿享生活' THEN '小李植栽'
        WHEN shop_name = '糀町💮植葉栽花種介' THEN '糀町植葉'
        WHEN shop_name = '糀町?植葉栽花種介' THEN '糀町植葉'
        WHEN shop_name = '?南犬?植栽_觀葉｜雨林｜家居擺飾｜' THEN '南犬植栽'
        WHEN shop_name = '🔰南犬🔰植栽_觀葉｜雨林｜家居擺飾｜' THEN '南犬植栽'
        WHEN shop_name = 'Mushi 沐時園藝' THEN '沐時園藝'
        WHEN shop_name = '珍奇植物 CarnivoRUs' THEN '珍奇植物'
        WHEN shop_name = '麗都Lido Garden花園農場' THEN '麗都花園'
        WHEN shop_name = '宅栽' THEN '宅栽工作室'
        ELSE shop_name
    END;
""")
print(f'已於{date}完成競品賣場的資料&名稱更新！','競品總數量' + str(len(keyword)))

page=[4, 10, 8, 3, 3, 3, 1]
href=['dicsp','mat1990m','a219787','paz.pan','sunshine.plant.art','yab7829','raising_trees']
keyword = ['麗都Lido Garden花園農場',"珍奇植物 CarnivoRUs","開心農元 Nursery & Garden Center","糀町💮植葉栽花種介","Mushi 沐時園藝","小李植栽 - 觀葉植物專賣店 - 種好種滿享生活","🔰南犬🔰植栽_觀葉｜雨林｜家居擺飾｜"]
date = datetime.now().date()


# 商品已售出
for i in range(len(keyword)):
    print(f"第{i+1}個競品資料")
    for k in range(int(page[i])):
        itemid = []
        shopid =[]
        name = []
        price = []
        historical_sold = []
        link=[]
        shop_name=[]
        monthly_sales="0"
        print(f"{keyword[i]}第{k+1}頁面")
        time.sleep(random.randint(30, 40))
        driver.get(f'https://shopee.tw/{href[i]}?page={str(k)}sortBy=pop') 
        time.sleep(random.randint(100,150))

        for scroll in range(20):
            driver.execute_script('window.scrollBy(0,1000)')
            time.sleep(random.randint(40, 55))
            
        for item, thename in zip (driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="link"]'),
                                driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="name"]')):
                # Link/ItemID/shopID
                getID = item.get_attribute('href')
                theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
                theshopid = int(getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')]) 
                link.append(getID)
                itemid.append(theitemid)
                shopid.append(theshopid)
                shop_name.append(keyword[i])
            
                
                # 商品名稱
                getname = thename.text.split('\n')[0]
                name.append(getname)
                time.sleep(random.randint(10, 15))

                thecontent = item.text
                thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
                thecut = thecontent.split('\n')
                
                # 商品價格
                if len(thecut) >= 3:
                    if bool(re.search('市|區|縣|鄉|海外|中國大陸', thecontent)): #有時會沒有商品地點資料
                        if bool(re.search('已售出', thecontent)): #有時會沒銷售資料
                            if '出售' in thecut[-3][1:]:
                                theprice = thecut[-4][1:]
                            else:
                                theprice = thecut[-3][1:]
                        else:
                            theprice = thecut[-2][1:]
                    else:
                        if bool(re.search('已售出', thecontent)):
                            theprice = thecut[-2][1:]
                        else:
                            theprice = thecut[-1][1:]               
                elif re.search('已售出', thecontent):   #有時會沒銷售資料
                    if len(thecut) == 1:
                        theprice = thecut[0]
                    else:
                        theprice = thecut[-2][1:]
                elif len(thecut)==2:
                        theprice = thecut[-1]
                else:                               # 處理 thecut 列表不足 3 個元素的情況（例如將 theprice 設置為空字符串）
                    theprice = ''

                theprice = theprice.replace('$','')
                theprice = theprice.replace('已','')
                theprice = theprice.replace(',','')
                theprice = theprice.replace('售','')
                theprice = theprice.replace('出','')
                theprice = theprice.replace(' ','')
                if '萬' in theprice:
                    theprice=int(float(theprice.replace('萬',""))*10000)
                if ' - ' in theprice:
                    theprice = (int(theprice.split(' - ')[0]) +int(theprice.split(' - ')[1]))/2
                if '-' in theprice:
                    theprice = (int(theprice.split('-')[0]) +int(theprice.split('-')[1]))/2
                if theprice != '':
                    price.append(int(theprice))
                else:
                    price.append(0)
                    print(0)
        # 取得已售出
        # get_historical_sold = driver.find_elements(By.CSS_SELECTOR, '.shop-search-result-view [class="rOgDNT lNPX0P"]')
        get_historical_sold = driver.find_elements(By.XPATH, "//div[@class='shop-search-result-view']//*[contains(text(),'已售出')]")
        for element in get_historical_sold:
            content_historical_sold = element.text
            print(content_historical_sold)
            if content_historical_sold == "":
                historical_sold.append(0)
                print(0)
            elif '萬' in content_historical_sold :
                content_historical_sold = float(content_historical_sold.replace("已售出 ", "").replace(",","").replace(".","").replace("萬",""))*10000
                historical_sold_value = int(content_historical_sold)
                historical_sold.append(historical_sold_value)

            else:
                content_historical_sold = float(content_historical_sold.replace("已售出 ", "").replace(",",""))
                historical_sold_value = int(content_historical_sold)
                historical_sold.append(historical_sold_value)

        max_length = len(itemid)
        add_num=max_length-len(historical_sold)
        historical_sold=historical_sold+[None] * add_num

        for it in range(len(itemid)):
            values = (str(date), itemid[it], name[it], shopid[it], shop_name[it], price[it], historical_sold[it], monthly_sales)
            sql = 'INSERT INTO products_info (date, product_id, product_name, shop_id, shop_name, price, historical_sales, monthly_sales ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                SQLcommand().modify_tuple(sql, values)
            except Exception as e:
                if historical_sold[it] is None:
                    pass
                else:
                    print(f"{itemid[it]}{name[it]},歷史銷售量:{historical_sold[it]}")
                print(f"發生異常: {e}")
        print(f'已於{date}完成{keyword[i]}第{[k+1]}頁歷史銷售資料更新！','總銷售商品數' + str(len(itemid)))


#取得商品月銷量資訊
for i in range(len(keyword)):
    print(f"第{i+1}個競品資料的月銷量")
    for k in range(int(page[i])):
        itemid = []
        monthly_sales= []
        print(f"{keyword[i]}第{k+1}頁面")
        driver.get(f'https://shopee.tw/{href[i]}?page={str(k)}&sortBy=sales' )
        time.sleep(random.randint(100,150))

        # 滾動頁面
        for scroll in range(10):
            driver.execute_script('window.scrollBy(0,1000)')
            time.sleep(random.randint(50,70))
        #取得商品內容
        for item, thename in zip (driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="link"]'),
                                  driver.find_elements(By.CSS_SELECTOR,'.shop-search-result-view [data-sqe="name"]')):
            getID = item.get_attribute('href')
            
            theitemid = int((getID[getID.rfind('.')+1:getID.rfind('?')]))
            itemid.append(theitemid)

    # 取得月銷量
        get_mounthly_sales = driver.find_elements(By.CSS_SELECTOR, ".shop-search-result-view div.rOgDNT")
        for element in get_mounthly_sales:
            content_monthly = element.text
            if content_monthly == "":
                monthly_sales.append(0)
            else:
                content_monthly = content_monthly.replace("月銷量", "").replace(",","")
                mounthly_sales_value = int(content_monthly)
                monthly_sales.append(mounthly_sales_value)

        max_length = len(itemid)
        add_num=max_length-len(monthly_sales)
        monthly_sales=monthly_sales+[None] * add_num

        for ite in range(len(itemid)):
            values = (monthly_sales[ite], itemid[ite])
            sql = "UPDATE products_info SET monthly_sales = %s WHERE product_id = %s"
            try:
                SQLcommand().modify_tuple(sql, values)
            except Exception as e:
                if monthly_sales[ite] is None:
                    pass
                else:
                    print(f"{itemid[ite]},月銷售量:{monthly_sales[ite]}")    
                print(f"發生異常: {e}")
       
        print(f'已於{date}完成{keyword[i]}第{[k+1]}頁的月銷售資料更新！','總銷售商品數' + str(len(itemid)))      
        
SQLcommand().modify("""
    UPDATE products_info
    SET shop_name = CASE
        WHEN shop_id = '3045968' THEN '開心農元'
        WHEN shop_id = '7432754' THEN '小李植栽'
        WHEN shop_id = '369371665' THEN '糀町植葉'
        WHEN shop_id = '268986085' THEN '南犬植栽'
        WHEN shop_id = '161364427' THEN '沐時園藝'
        WHEN shop_id = '15227497' THEN '珍奇植物'
        WHEN shop_id = '4877504' THEN '麗都花園'
        WHEN shop_id = '145300134' THEN '宅栽工作室'
        ELSE shop_name
    END;
""")
print(f'所有資料已匯入資料庫且同步完成products_info表格的名稱更新')
driver.close() 




