import os
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def load_embeddings():

    persist_directory = "./chroma_db"


    # Re-initialize the exact same embedding model used during creation
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    try:

        # Loading the Chroma 
        database = Chroma(

            persist_directory = persist_directory,
            embedding_function = embedding_model

        )

        retriever = database.as_retriever()

        return retriever

    except Exception as e:

        #print(f"Error loading LangChain Chroma vector store: {e}")
        
        raise 
