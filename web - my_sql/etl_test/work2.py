import requests
import pandas as pd
from IPython.display import clear_output
# 與伺服器做連線
# 讓104 不要以為我們是爬蟲 於是新增 User-Agent 還有 Referer ， Referer 指的是前一次造訪的網頁
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Referer": "https://www.104.com.tw/"
}
url = "https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword=爬蟲工程師&expansionType=area,spec,com,job,wf,wktm&order=12&asc=0&page=4&mode=l&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
resp = requests.get(url, headers=headers)
# 這段可以叫出所有key值
# print(resp.json()["data"].keys())
# print(pd.DataFrame(resp.json()["data"]['list']))
df = []
for page in range(1,10):
    url = "https://www.104.com.tw/jobs/search/list?ro=0&kwop=7&keyword=爬蟲工程師&expansionType=area,spec,com,job,wf,wktm&order=12&asc=0&page={page}&mode=l&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
    # print(url)
    resp = requests.get(url, headers=headers)
    # 用 pd 去把資料做整理
    ndf = pd.DataFrame(resp.json()["data"]["list"])[['jobName', 'jobNameSnippet', 'jobAddrNoDesc', 'jobAddress', 'custNameRaw']]
    df.append(ndf)
    # if ndf.shape[0] < 30:
    #     break
# 把爬出來的資料整合排列
df = pd.concat(df, ignore_index=True)
print(df)