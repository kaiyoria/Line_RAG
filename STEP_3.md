# 整合 Line 機器人與 Groq API

我使用 PyCharm 在本地端撰寫並執行程式，然而 Line 機器人必須透過 webhook 接收用戶發送的訊息，為了讓本地端服務能夠對外開放，我使用 Flask 架設 HTTP 伺服器，透過 ngrok 將本地的埠號導向一個可供外部連線的公開網址。藉由此方法，Line 的 webhook 能夠順利將事件傳送到本地伺服器，實現與用戶的即時互動。

### 1.下載 ngrok
* [造訪 ngrok 官方網站（需註冊）](https://ngrok.com/)
* 選擇下載 Download for Windows (64-Bit)。解壓縮後獲得`ngrok.exe`。
* 回到網站，點擊 Your Authtoken，複製 Command Line 下的 Authtoken。
* 開啟命令提示字元，切換到 `ngrok.exe` 所在資料夾，輸入 Authtoken。
* 完成輸入後，會看到以下訊息：
  ```
  Authtoken saved to configuration file: C:\Users\你的使用者名稱\.ngrok2\ngrok.yml
  ```
>圖1-10.下載 Download for Windows (64-Bit)
>
><img src="Photos/RAG_10.jpg" alt="RAG流程圖" width="500" height="220"/>

>圖1-11.命令提示字元使用的 Authtoken
>
><img src="Photos/RAG_11.jpg" alt="RAG流程圖" width="650" height="250"/>

### 2.實作 LINE 機器人後端系統
* [實作檔案](Code/app.py)
* 請先安裝以下套件：
```
pip install flask            #建立一個能接收網路訊息並回應的伺服器
pip install line-bot-sdk     #Line Messaging API 的官方 Python SDK
pip install python-dotenv    #載入 .env 檔案中的 API 金鑰
```
* 功能介紹：整合 Groq OpenAI 聊天函式製作 LINE 聊天機器人後端服務。
  * 使用 `dotenv` 套件讀取 `.env` 檔案中的環境變數：
    * `LINE_CHANNEL_ACCESS_TOKEN`：LINE 機器人頻道的存取權。
    * `LINE_CHANNEL_SECRET`：LINE 頻道的密鑰，用於驗證 webhook 請求合法性。
  * 使用 `Flask` 建立一個本地 Web 伺服器，監聽 `/callback` 路由，接收來自 LINE 平台的 webhook 請求。
  * 利用 `line-bot-sdk` 中的 `WebhookHandler` 驗證來自 LINE 的簽名，確保訊息安全。
  * 註冊訊息事件處理函式，當收到用戶文字訊息時：
    * 取得用戶傳來的文字內容
    * 呼叫自訂的 `mychatbot` 函式（來源於 `groq_openapi` 模組），取得聊天回覆
    * 利用 `line_bot_api.reply_message()` 回覆文字訊息給用戶
  * 當直接執行程式時，啟動 Flask 伺服器監聽本機 5000 埠口。

[上一頁](STEP_2.md)| [目錄](README.md) |[下一頁](STEP_4.md)
