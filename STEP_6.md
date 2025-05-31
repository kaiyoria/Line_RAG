# 六、一鍵啟動 Line 機器人
啟動機器人流程過於繁瑣，需依序完成多個步驟：先執行主程式，再手動開啟 Ngrok 並輸入埠號，最後還需將產生的網址貼至 Line Developers 進行 Webhook 驗證，整個啟動流程才能完成。為簡化上述流程，本檔案整合了 Flask 伺服器啟動、Ngrok 埠口轉發、以及 Line Webhook 自動設定等功能，可一鍵完成所有必要操作。

* 實作檔案(Code/dev_server.py)
* 

---
[上一頁](STEP_5.md)| [目錄](README.md) |[下一頁](STEP_7.md)
