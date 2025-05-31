# 六、一鍵啟動 Line 機器人
啟動機器人流程過於繁瑣，需依序完成多個步驟：先執行主程式，再手動開啟 Ngrok 並輸入埠號，最後還需將產生的網址貼至 Line Developers 進行 Webhook 驗證，整個啟動流程才能完成。為簡化上述流程，本檔案整合了 Flask 伺服器啟動、Ngrok 埠口轉發、以及 Line Webhook 自動設定等功能，可一鍵完成所有必要操作。

### 系統架構與功能設計

* 實作檔案(Code/dev_server.py)
* 使用`subprocess`模組啟動兩個子行程：
  * `appV2.py`(主程式)
  * `ngrok http 5000`(產生公開網址)
* 從 Ngrok 回傳的所有資料中，找出`https`協定並回傳它的公開網址。
* 若在開啟 Ngrok 後在瀏覽器輸入以下網址，能看到程式提及的 JSON 內容：
```
http://localhost:4040/api/tunnels
```
* 將回傳網址加上`/callback`路徑，透過 HTTP PUT 請求呼叫 LINE 官方 API，設定 Webhook Endpoint。
  * API 端點：`https://api.line.me/v2/bot/channel/webhook/endpoint`
  * 認證方式：在`Authorization`標頭中加入`Bearer {你的 Channel Access Token}`

### 執行方式

1. 備妥：
   * `ngrok.exe`可執行檔放於當前目錄或已加入系統 PATH。
   * `.env`檔案中包含`LINE_CHANNEL_ACCESS_TOKEN`。
2. 執行`dev_server.py`
3. 成功啟動後，畫面會顯示：
   ```bash
   🌐 Ngrok 公開網址：https://xxxxx.ngrok.io
   ✅ LINE Webhook 設定完成：https://xxxxx.ngrok.io/callback
   🚀 已啟動 Flask + Ngrok + LINE Webhook
   ```

---
[上一頁](STEP_5.md)| [目錄](README.md) |[下一頁](STEP_7.md)
