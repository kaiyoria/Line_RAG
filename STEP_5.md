# 整合 RAG 系統與 Line 機器人
透過 Line 介面與 RAG 系統互動，將爬蟲、向量資料庫與語言模型生成功能串接至 Line 機器人，製作可即時對話的生活優惠查詢助手。

### 1.系統架構與功能設計
* [實作檔案](Code/appV2.py)
* 使用`Flask`建立本地伺服器，接收 LINE Webhook 訊息並進行處理。
* 用戶訊息事件依照輸入內容分流執行：
  * `幫助 / 說明` → 顯示使用方式與功能列表。
  * `更新 / 資料` → 呼叫`PTTcrawler.py`及`FAISS.py`更新 PTT 資料與向量庫。
  * 其他訊息 → 呼叫 `chat_with_rag()` 啟動 RAG 模型進行語意檢索與問答生成。
* 程式執行後開啟本地端 5000 埠口，透過 Ngrok 建立外部可連接網址供 LINE 使用。

### 2.結果
* 當訊息文字內出現幫助/說明，會出現使用方法說明：
* 首次加入好友時也會出現。
<div style="display: flex; justify-content: space-between;">
  <img src="Photos/RAG_17.jpg" alt="RAG流程圖2" width="480" height="600"/>
  <img src="Photos/RAG_18.jpg" alt="RAG流程圖3" width="480" height="600"/>
</div>


---
[上一頁](STEP_4.md)| [目錄](README.md) |[下一頁](STEP_6.md)
