# chatbot.py

import os
import getpass
from langchain.chat_models import init_chat_model
from embeddings import load_embeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.runnables import RunnableSequence
from langchain import hub
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import HumanMessagePromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

if not os.environ.get("GOOGLE_API_KEY"):

    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

# Initialize LLM 
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=1.0)

retriever = load_embeddings()

#rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

contextualize_q_system_prompt = (
    
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([

    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),

])

history_aware_retriever = create_history_aware_retriever(

    llm=llm,
    retriever=retriever,
    prompt=contextualize_q_prompt

)

qa_system_prompt = (

    "1. You are an assistant specializing in Emotional Well-being and Mental Health, providing empathetic and accurate support.\n"
    "2. Use the provided context to answer the question concisely and relevantly. If the context is unrelated to the query, respond based on your mental health knowledge.\n"
    "3. For questions outside emotional or mental health, state: \"This question is a bit outside what I can help with, but I’m here if you’d like to talk about anything related to how you’re feeling or your emotional well-being.\"\n"
    "4. If you lack sufficient information, say: \"I don't have enough information to answer this.\"\n"
    "5. Keep responses between three and five sentences with a compassionate tone.\n"
    "6. If the user expresses thoughts of self-harm, harming others, or shows signs of severe emotional distress, respond with empathy and urge them to seek immediate help from a licensed mental health professional or contact a crisis support service in their area.\n"
    "7. If the user expresses intent to harm others or shows signs of aggressive behavior, respond calmly and compassionately. Do not attempt to assess or intervene. Gently encourage the user to seek immediate help from a licensed mental health professional or contact emergency services if someone is in danger.\n"
    "{context}"

)

qa_prompt = ChatPromptTemplate.from_messages([

    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),

])

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

memory = ChatMessageHistory()

# Wrapping rag_chain with RunnableWithMessageHistory using the single memory instance

conversational_rag_chain = RunnableWithMessageHistory(

    rag_chain,
    lambda _: memory,  # Use single memory instance
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"

)

# Generate_response function with default session_id
def generate_response(user_input: str) -> str:

    try:
        # Retrieving chat history
        chat_history = memory.messages

        # Invoking the conversational RAG chain 
        result = conversational_rag_chain.invoke(

            {"input": user_input, "chat_history": chat_history},
            config={"configurable": {"session_id": "default"}} 
        )

        # Extracting bot's response
        ai_response = result["answer"]

        # Store in memory
        memory.add_user_message(user_input)
        memory.add_ai_message(ai_response)

        return ai_response

    except Exception as e:

        import traceback

        traceback.print_exc()
        return f"❌ An error occurred while generating the response: {e}"
