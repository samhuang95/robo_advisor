# 抓取 PTT 電影版的網頁原始碼 (HTML)
import urllib.request as req
url = "https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=%E7%88%AC%E8%9F%B2%E5%B7%A5%E7%A8%8B%E5%B8%AB&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=14&asc=0&page=2&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob="
# 建立一個 Request 物件， 附加 Request Headers 的資訊
request = req.Request(url, headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
})
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")


# 解析原始碼, 取得每篇文章的標題
import bs4
root = bs4.BeautifulSoup(data, "html.parser")
titles = root.find_all("div", class_="title") #尋找 class = "titles" 的 div 標籤 find_all找出所有的 find 找出一個
for title in titles:
    if title.a != None: #  如果標題包含 a 標籤 (沒有被印刪除). 印出來
        print(title.a.string)
    