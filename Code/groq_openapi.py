import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 載入.env環境變數檔

model = "llama-3.3-70b-versatile"
client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

messages = [{"role": "system", "content": "請用中文回覆我，你是有幫助的LINE助手"}]

def mychatbot(prompt):
    messages.append({"role": "user", "content": prompt})
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    reply = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply
