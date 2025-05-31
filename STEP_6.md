# 六、一鍵啟動 Line 機器人
啟動機器人流程過於繁瑣，需依序完成多個步驟：先執行主程式，再手動開啟 Ngrok 並輸入埠號，最後還需將產生的網址貼至 Line Developers 進行 Webhook 驗證，整個啟動流程才能完成。為簡化上述流程，本檔案整合了 Flask 伺服器啟動、Ngrok 埠口轉發、以及 Line Webhook 自動設定等功能，可一鍵完成所有必要操作。

### 系統架構與功能設計

* [實作檔案](Code/dev_server.py)
* 使用`subprocess`模組啟動兩個子行程：
  * `appV2.py`(主程式)
  * `ngrok http 5000`(產生公開網址)
* 從 Ngrok 回傳的所有資料中，找出`https`協定並回傳它的公開網址。
* 在開啟 Ngrok 後，於瀏覽器中輸入以下網址，可查看對應的 JSON 資料內容：
```
http://localhost:4040/api/tunnels
```
* 將回傳網址加上`/callback`，透過 HTTP 請求向 LINE API 更新 webhook 設定。
  * Line API 端點：`https://api.line.me/v2/bot/channel/webhook/endpoint`
  * 認證方式：在`Authorization`標頭中加入`Bearer {你的 Channel Access Token}`

### 執行方式

1. 備妥：
   * `ngrok.exe`與`dev_server.py`放在相同資料夾中。
   * `.env`檔案中包含`LINE_CHANNEL_ACCESS_TOKEN`。
2. 執行`dev_server.py`
3. 成功啟動後，畫面會顯示：
   ```bash
   🌐 Ngrok 公開網址：https://xxxxx.ngrok.io
   ✅ LINE Webhook 設定完成：https://xxxxx.ngrok.io/callback
   🚀 已啟動 Flask + Ngrok + LINE Webhook
   ```

---
[上一頁](STEP_5.md)| [目錄](README.md) |[下一頁](ADD_1.md)
