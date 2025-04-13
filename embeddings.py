# -*- coding: utf-8 -*-
"""embeddings.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1msRPZ8GQTtxps7DReDBBwluT7mHzUj02
"""

# embeddings.py
from langchain_core.embeddings import Embeddings
from google import generativeai as genai
from langchain_community.vectorstores import Chroma
import os
from langchain_community.vectorstores import Chroma
# Other imports...


os.environ["GOOGLE_API_KEY"] = "qeZc"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

class GeminiEmbeddings(Embeddings):
    def __init__(self, model_name="models/embedding-001"):
        self.model_name = model_name

    def embed_documents(self, texts):
        return [
            genai.embed_content(model=self.model_name, content=t, task_type="retrieval_document")["embedding"]
            for t in texts
        ]

    def embed_query(self, text):
        return genai.embed_content(model=self.model_name, content=text, task_type="retrieval_query")["embedding"]

# Load the retriever from disk
embedding = GeminiEmbeddings()
db = Chroma(embedding_function=embedding)  # In-memory mode

retriever = db.as_retriever(search_kwargs={"k": 3})
