# 登入蝦皮流程
from pandas import options
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumwire import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException

username = 'flychenjack01'
password = 'Qqaz0911'
# username = 'samhuangworkshop'
# password = 'Ss99236567'
# 商品表現網頁
url = 'https://shopee.tw/seller/login?next=https%3A%2F%2Fseller.shopee.tw%2Fdatacenter%2Fproducts%2Fanalysis%2Fperformance'

# 避免 chrome 跳出要求權限的顯示通知
# 創建 Preferences 物件
option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)

#設定Chrome選項-啟動headless模式
option.add_argument('--headless')
option.add_argument('--no-sandbox')

# prefs = {
#     'profile.default_content_setting_values.notifications': 2,
#     'profile.default_content_settings.popups': 0,
#     'download.default_directory': '/path/to/download/directory',
#     'profile.default_content_setting_values.automatic_downloads': 1
# }

# option.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(chrome_options = option)
driver.get(url)

# 登入結果會直接進入到商品 > 商品表現
time.sleep(random.randint(15, 20))
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(username)
time.sleep(random.randint(2, 4))
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(random.randint(2, 4))
driver.find_elements(By.CSS_SELECTOR, 'button')[2].click()

# 自動化抓取資料
# -----------------------------------------------
## update product_detail data
# 進到商品>商品表現
time.sleep(random.randint(20., 30.))
# 選擇日期
element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 選擇昨天
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(40., 50.))
# 點擊下載
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[2]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
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
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[12]
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
element = driver.find_elements(By.CLASS_NAME ,'shopee-date-shortcut-item')[1]
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(40., 50.))
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

element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[9]
driver.execute_script("arguments[0].click();", element)


time.sleep(random.randint(3., 6.))
# 選擇日期
element = driver.find_element(By.CLASS_NAME ,'bi-date-input')
driver.execute_script("arguments[0].click();", element)

time.sleep(random.randint(3., 6.))
# 點掉教學蓋板
element = driver.find_elements(By.CLASS_NAME ,'shopee-button')[4]
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



