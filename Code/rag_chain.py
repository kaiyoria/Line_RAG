from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # 載入.env環境變數檔

class CustomE5Embedding(HuggingFaceEmbeddings):
    def embed_documents(self, texts):
        texts = [f"passage: {t}" for t in texts]
        return super().embed_documents(texts)

    def embed_query(self, text):
        return super().embed_query(f"query: {text}")

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "faiss_db")

embedding_model = CustomE5Embedding(model_name="intfloat/multilingual-e5-small")
db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

system_prompt = (
    "請用台灣人習慣的中文回答以下問題。"
    "你是一位生活理財專家，擅長分析 PTT Lifeismoney 省錢板上的資訊。"
    "請幫助使用者從眾多優惠或討論中，整理出最有幫助的省錢建議。"
)

prompt_template = """
以下是從 PTT Lifeismoney 板上找到的相關討論內容：{retrieved_chunks}
請使用台灣人習慣的中文回覆，根據這些內容，協助使用者回答下列問題：{question}
請模仿以下語氣來回覆：
- 開頭請說：「優惠嗎?我找找看!」
- 回答後請加上一句：「如果去 PTT Lifeismoney 板的話，能找到更詳細的優惠喔！」
若沒有足夠資訊，請誠實告知，並建議使用者前往原文查詢。
"""

model = "llama-3.3-70b-versatile"
base_url = "https://api.groq.com/openai/v1"
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url=base_url)

def chat_with_rag(user_input: str) -> str:
    docs = retriever.get_relevant_documents(user_input)
    retrieved_chunks = "\n\n".join([doc.page_content for doc in docs])
    final_prompt = prompt_template.format(retrieved_chunks=retrieved_chunks, question=user_input)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt}
        ]
    )
    return response.choices[0].message.content

#if __name__ == "__main__":
    #print(chat_with_rag('最近有沒有咖啡的購買優惠 ?'))
