import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class CustomE5Embedding(HuggingFaceEmbeddings):
    def embed_documents(self, texts):
        texts = [f"passage: {t}" for t in texts]
        return super().embed_documents(texts)
    def embed_query(self, text):
        return super().embed_query(f"query: {text}")

target_file = "ptt_lifeismoney_100.txt"

loader = TextLoader(target_file, encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_docs = splitter.split_documents(documents)

embedding_model = CustomE5Embedding(model_name="intfloat/multilingual-e5-small")
vectorstore = FAISS.from_documents(split_docs, embedding_model)
vectorstore.save_local("faiss_db")

print("向量資料庫已建立並儲存於 'faiss_db/' 目錄中。")
