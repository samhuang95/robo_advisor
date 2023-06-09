# 登入蝦皮流程
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

username = 'userID'
password = 'user_password'
# 商品表現網頁
url = 'https://shopee.tw/seller/login?next=https%3A%2F%2Fseller.shopee.tw%2Fdatacenter%2Fproducts%2Fanalysis%2Fperformance'

service = ChromeService(executable_path='./chromedriver.exe')

option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)

# 避免 chrome 跳出要求權限的顯示通知
# 創建 Preferences 物件
# 設定下載路徑
download_path = "D:\\robo_advisor\\robo_advisor\\docker\\app\\functions\\ETL_update_shopee_data\\csv_download"
prefs = {
    'profile.default_content_setting_values.notifications': 2,
    'profile.default_content_settings.popups': 0,
    'download.default_directory': download_path,
    'profile.default_content_setting_values.automatic_downloads': 1
}

driver = webdriver.Chrome(options=option)
driver.get(url)

time.sleep(random.randint(5., 10.))
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(username)
time.sleep(random.randint(2, 4))
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(random.randint(1,3))
driver.find_elements(By.CSS_SELECTOR, 'button')[2].click()

# 結果會直接進入到商品 > 商品表現

# 自動化抓取資料
# -----------------------------------------------
## update product_detail data
# 進到商品>商品表現
time.sleep(random.randint(20., 30.))
# 關閉教學
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[71]
driver.execute_script("arguments[0].click();", element) 

# 進到商品>商品表現
time.sleep(random.randint(3., 6.))
# 選擇日期
element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇昨天
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(45., 50.))
# 點擊下載
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[2]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(20., 30.))
# 下載
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[4]
driver.execute_script("arguments[0].click();", element)

# -----------------------------------------------
## update product_overview data

time.sleep(random.randint(3., 6.))
# 進到商品>商品指標
element = driver.find_elements(By.CLASS_NAME ,'side-navbar-item')[0]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 點掉教學蓋板
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[10]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇日期
element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇昨天
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(40., 50.))
# 點擊下載
element = driver.find_elements(By.CLASS_NAME ,'track-click-normal-export')[0]
driver.execute_script("arguments[0].click();", element)

# -----------------------------------------------
## update traffic_overview data

time.sleep(random.randint(3., 6.))
# 進到流量總攬
element = driver.find_elements(By.CLASS_NAME ,'nav-tab')[3]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇日期
element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇昨天
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[0]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(50., 55.))
# 點擊下載
element = driver.find_elements(By.CLASS_NAME ,'track-click-normal-export')[0]
driver.execute_script("arguments[0].click();", element)

# -----------------------------------------------
## update stats data

time.sleep(random.randint(3., 6.))
# 進到數據總覽
element = driver.find_elements(By.CLASS_NAME ,'nav-tab')[0]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 點掉更新公告、歡迎頁
try:
    element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[9]
    driver.execute_script("arguments[0].click();", element)
except:
    pass

time.sleep(random.randint(3., 6.))
# 選擇日期
try:
    element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
    driver.execute_script("arguments[0].click();", element)
except:
    pass

time.sleep(random.randint(3., 6.))
# 點掉教學蓋板
try:
    element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[4]
    driver.execute_script("arguments[0].click();", element)
except:
    pass


time.sleep(random.randint(3., 6.))
# 選擇日期
try:
    element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
    driver.execute_script("arguments[0].click();", element)
except:
    pass

time.sleep(random.randint(3., 6.))
# 選擇昨天
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(45., 50.))
# 點擊下載
element = driver.find_element(By.CLASS_NAME ,'track-click-normal-export')
driver.execute_script("arguments[0].click();", element)
# -----------------------------------------------
## make sure data file is exist or not 

from datetime import timedelta
import datetime
import os

now = datetime.datetime.now().date()
yesterday = now - timedelta(days=1)
year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

product_overview = f'[export_report]productoverview{year}{month}{day}-{year}{month}{day}.xlsx'
product_detail = f'export_report.parentskudetail.{year}{month}{day}_{year}{month}{day}.xlsx'
traffic_overview = f'[export_report]traffic_overview_{year}{month}{day}_{year}{month}{day}.xlsx'
stats = f'flychenjack01.shopee-shop-stats.{year}{month}{day}-{year}{month}{day}.xlsx'

if not os.path.isfile(os.path.join(download_path, product_overview)):
    time.sleep(random.randint(3., 6.))
    # 進到商品>商品指標
    element = driver.find_elements(By.CLASS_NAME ,'side-navbar-item')[0]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇日期
    element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇昨天
    element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(50., 55.))
    # 點擊下載
    element = driver.find_elements(By.CLASS_NAME ,'track-click-normal-export')[0]
    driver.execute_script("arguments[0].click();", element)
    print('product_overview download again')
else:
    print('product_overview is exist')


if not os.path.isfile(os.path.join(download_path, product_detail)):
    # 進到商品
    element = driver.find_elements(By.CLASS_NAME ,'nav-tab')[1]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 關閉教學
    element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[10]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 進到商品指標
    element = driver.find_elements(By.CLASS_NAME ,'side-navbar-item')[1]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇日期
    element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇昨天
    element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(45., 50.))
    # 點擊下載
    element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[2]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(20., 30.))
    # 下載
    element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[4]
    driver.execute_script("arguments[0].click();", element)
    print('product_detail download again')
else:
    print('product_detail is exist')

if not os.path.isfile(os.path.join(download_path, traffic_overview)):
    time.sleep(random.randint(3., 6.))
    # 進到流量總攬
    element = driver.find_elements(By.CLASS_NAME ,'nav-tab')[3]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇日期
    element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 選擇昨天
    element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[0]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(50., 55.))
    # 點擊下載
    element = driver.find_elements(By.CLASS_NAME ,'track-click-normal-export')[0]
    driver.execute_script("arguments[0].click();", element)
    print('traffic_overview download again')
else:
    print('traffic_overview is exist')

if not os.path.isfile(os.path.join(download_path, stats)):
    time.sleep(random.randint(3., 6.))
    # 進到數據總覽
    element = driver.find_elements(By.CLASS_NAME ,'nav-tab')[0]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(3., 6.))
    # 點掉更新公告、歡迎頁
    try:
        element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[9]
        driver.execute_script("arguments[0].click();", element)
    except:
        pass
    time.sleep(random.randint(3., 6.))
    # 選擇日期
    try:
        element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
        driver.execute_script("arguments[0].click();", element)
    except:
        pass
    time.sleep(random.randint(3., 6.))
    # 點掉教學蓋板
    try:
        element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[4]
        driver.execute_script("arguments[0].click();", element)
    except:
        pass
    time.sleep(random.randint(3., 6.))
    # 選擇日期
    try:
        element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
        driver.execute_script("arguments[0].click();", element)
    except:
        pass
    time.sleep(random.randint(3., 6.))
    # 選擇昨天
    element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.randint(45., 50.))
    # 點擊下載
    element = driver.find_element(By.CLASS_NAME ,'track-click-normal-export')
    driver.execute_script("arguments[0].click();", element)
    print('stats download again')
else:
    print('stats is exist')

# 關閉瀏覽器
driver.quit()