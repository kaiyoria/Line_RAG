# 二、整合 Line 機器人與 Groq API 系統
本專案使用 PyCharm 作為主要的程式編輯與執行環境

### 1.註冊Groq API
* 搜尋 Groq PlayGround ->點選 API KEYS -> Create API Key ->**複製 API Key**

### 2. 建立存放金鑰匙的文件
* 建立`.env`檔，將先前獲得的 Channel secret、Channel access token、Groq API key貼上`.env`檔內，如下：

```
LINE_CHANNEL_ACCESS_TOKEN=(輸入您的LINE_CHANNEL_ACCESS_TOKEN)
LINE_CHANNEL_SECRET=(輸入您的LINE_CHANNEL_SECRET)
GROQ_API_KEY=(輸入您的GROQ_API_KEY)
```

[上一頁](STEP_1.md)| 第三頁 |[下一頁]
