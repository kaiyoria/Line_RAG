# 四、建立 RAG 系統
問答機器人已完成初步功能，接下來預計導入 RAG 架構，資料來源為 PTT Lifeismoney 版。PTT Lifeismoney 版內有許多鄉民會提供生活上的優惠資訊，如：7-11咖啡優惠、免費Line貼圖等等，可作為RAG的知識基礎。

### 1.PTT 爬蟲程式
為了獲得最新最有價值的資料，從 Lifeismoney 版內抓取最新的100篇文章標題和內文。
* [實作檔案](Code/PTTcrawler.py)
* 使用`requests`和`BeautifulSoup`套件向 PTT 發送請求並解析 HTML 內容。
* 透過迴圈逐頁往前翻頁，直到蒐集滿 100 篇文章為止。
* 移除文章中的推文與版頭資訊，只保留純內文。
* 將結果依序寫入`ptt_lifeismoney_100.txt`，提供後續 RAG 使用。
* 執行完成，會顯示：
```
所有文章已存入ptt_lifeismoney_100.txt
```

### 2. 建立向量資料庫
將爬下來的`ptt_lifeismoney_100.txt`進行切分、語意向量化，並使用 FAISS 建立可供檢索的向量資料庫。

* [實作檔案](Code/FAISS.py)
* 使用`LangChain` 提供的 `TextLoader`載入文字檔內容。
* 使用`RecursiveCharacterTextSplitter`將長文本切分為重疊區塊(chunk size=500, overlap=100)，以保留語境。
* 採用 HuggingFace 上的`intfloat/multilingual-e5-small`模型進行向量嵌入。
  * 加上 `"passage:"` 與 `"query:"` 前綴，符合 E5 模型訓練方式。
* 使用 FAISS 建立向量索引，並儲存至本地目錄 `faiss_db/`。
* 執行完成，會顯示：
```
向量資料庫已建立並儲存於 'faiss_db/' 目錄中。
```

### 3. 啟動 RAG 問答流程
將使用者的問題與 FAISS 資料庫中的 PTT 文章進行語意匹配，結合`llama-3.3-70b-versatile`模型產生回覆。

* [實作檔案](Code/rag_chain.py)
* 使用`FAISS.load_local()`載入先前建立的向量資料庫 `faiss_db/`。
* 使用`CustomE5Embedding`確保查詢向量化時加入 `"query:"` 前綴，以符合 E5 格式。
* 建立檢索器`retriever`，能根據問題找到最相關的文章片段。
* 設定`prompt_template`和`system_prompt`，引導模型用台灣人習慣的語氣，並模仿生活理財達人的語氣回覆。



[上一頁](STEP_3.md)| [目錄](README.md) |[下一頁](STEP_5.md)
