import os
import subprocess
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from rag_chain import chat_with_rag

load_dotenv()

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

HELP_MESSAGE = """\
🤖 使用方法說明：

1️⃣ 輸入關鍵字查詢資訊  
例如：油價、LINE points、咖啡，我會回覆相關資訊。

2️⃣ 使用指定指令操作  
- 幫助／說明：查看本訊息規範。  
- 更新資料：從PTT更新最新文章與知識庫。  
- 問問題：直接輸入問題，我會自動回覆您。

3️⃣ 注意事項  
請避免輸入過於模糊或複雜的問題，系統優先回覆關鍵字匹配結果。  
資料來源於PTT Lifeismoney版，僅供參考。"""

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip().lower()

    if any(word in user_msg for word in ["幫助", "說明","你好"]):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=HELP_MESSAGE)
        )

    elif any(word in user_msg for word in ["更新", "資料"]):
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text="資料更新中，請稍候...")
        )
        try:
            subprocess.run(["python", "PTTcrawler.py"], check=True)
            subprocess.run(["python", "FAISS.py"], check=True)
            # 再推播「完成」文字
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text="資料更新完成！歡迎繼續提問")
            )
        except subprocess.CalledProcessError as e:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text=f"更新失敗：{e}")
            )

    else:
        reply = chat_with_rag(user_msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

if __name__ == "__main__":
    app.run(port=5000)
