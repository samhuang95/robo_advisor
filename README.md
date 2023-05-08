# robo_advisor 是一個商品銷售策略的儀表板
## ▍功能說明
> 資料獲取
* 蝦皮爬蟲(關鍵商品、競品賣家、個人賣場檔案下載)
* Facebook API 資料獲取
> 銷售模型
* 消費者選購關鍵要素
* 業績預測(針對關鍵產品預測)
> Facebook 圖文成效預測
* 圖片成效預測(預測模型訓練、驗證模型訓練)
* 文案成效預設
* 發文時段預測
> 儀錶板介面設計

## ▍檔案說明
> 文件分類<br>
* 依據各項功能劃分程式資料夾
* 數據資料夾
> 環境建構<br>
* 可以使用 docker-composed 安裝完成

# 環境建置說明
1. 將檔案拉至本地端
    ```
    git clone https://github.com/samhuang95/robo_advisor.git
    ```
2. 建立docker環境
    ```
    cd ./docker
    docker compose up -d
    ```
3. 建置完畢 http://localhost:5000/
