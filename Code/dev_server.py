import subprocess
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
NGROK_PORT = 5000

def start_flask():
    return subprocess.Popen(["python", "appV2.py"])

def start_ngrok():
    return subprocess.Popen(["ngrok", "http", str(NGROK_PORT)])

def get_ngrok_url():
    for _ in range(5):
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            tunnels = response.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
        except Exception:
            time.sleep(1)
    raise RuntimeError("⚠️ 無法取得 ngrok 公開網址")

def set_line_webhook(ngrok_url):
    webhook_url = f"{ngrok_url}/callback"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"endpoint": webhook_url}
    response = requests.put(
        "https://api.line.me/v2/bot/channel/webhook/endpoint",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        print(f"✅ LINE Webhook 設定完成：{webhook_url}")
    else:
        print("❌ 設定失敗：", response.text)

if __name__ == "__main__":
    flask_proc = start_flask()
    ngrok_proc = start_ngrok()

    try:
        ngrok_url = get_ngrok_url()
        print(f"🌐 Ngrok 公開網址：{ngrok_url}")
        set_line_webhook(ngrok_url)
        print("🚀 已啟動 Flask + Ngrok + LINE Webhook")
        flask_proc.wait()
    except KeyboardInterrupt:
        print("🛑 停止中...")
        flask_proc.terminate()
        ngrok_proc.terminate()
