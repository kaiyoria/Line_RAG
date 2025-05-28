# 整合 Line 機器人與 Groq API

我使用 PyCharm 在本地端撰寫並執行程式，然而 LINE Bot 必須透過 webhook 接收用戶發送的訊息，為了讓本地端服務能夠對外開放，我使用 Flask 架設 HTTP 伺服器，透過 ngrok 將本地的埠號導向一個可供外部連線的公開網址。藉由此方法，LINE 的 webhook 能夠順利將事件傳送到本地伺服器，實現與用戶的即時互動。

### 1.下載 ngrok
* [造訪 ngrok 官方網站（需註冊）](https://ngrok.com/)
* 選擇下載 Download for Windows (64-Bit)。解壓縮後獲得`ngrok.exe`。
* 回到網站，點擊 Your Authtoken，複製 Command Line 下的 Authtoken。
* 開啟命令提示字元，切換到 `ngrok.exe` 所在資料夾，輸入Authtoken。
* 完成輸入後，會看到以下訊息：
  ```
  Authtoken saved to configuration file: C:\Users\你的使用者名稱\.ngrok2\ngrok.yml
  ```
>圖1-10.下載 Download for Windows (64-Bit)
>
><img src="Photos/RAG_10.jpg" alt="RAG流程圖" width="500" height="220"/>

>圖1-11.命令提示字元使用的Authtoken
>
><img src="Photos/RAG_11.jpg" alt="RAG流程圖" width="650" height="250"/>


[上一頁](STEP_2.md)| [目錄](README.md) |[下一頁](STEP_4.md)
