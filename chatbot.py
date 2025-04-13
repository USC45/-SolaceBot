# -*- coding: utf-8 -*-
"""chat.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B0zcZp4Y3VTJTp3k7k9TCqmiYuYuf1Rl
"""



import os
from langchain_community.llms import OpenAI, GooglePalm  # Correct import
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain
from langchain.chains import LLMChain, SequentialChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings  # if used
# Update memory and LLMChain usage based on latest syntax


#!pip install langchain openai google-generativeai

from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from embeddings import retriever

import getpass
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyA0p-1w5LWhBH3t2DctVzhGhreq1d3qeZc"

# Now you can use the API key in your code:
api_key = os.environ["GOOGLE_API_KEY"]

# Example of how to use it with a library that requires the key.
import google.generativeai as genai

genai.configure(api_key=api_key)

gemini_llm1 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
gemini_llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.9)

def is_safe_input(user_input):
    banned_words = ["suicide", "kill myself", "end it all"]  # Expand this list
    for word in banned_words:
        if word.lower() in user_input.lower():
            return False
    return True

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

summary_prompt = PromptTemplate(
    input_variables=["user_question"],
    template="""
Summarize the following message to identify the user's emotional concern clearly:
{user_question}
Summary:
"""
)

answer_prompt = PromptTemplate(
    input_variables=["summarized_question"],
    template="""
You are a compassionate mental health support assistant.

Provide a **single, emotionally supportive** response to the following situation. Keep it concise (1–3 sentences max), avoid giving multiple suggestions unless asked, and sound warm and natural like a friend.

Situation:
{summarized_question}

Response:

"""
)
validate_or_rewrite_prompt = PromptTemplate(
    input_variables=["user_input", "bot_response"],
    template="""
You are a helpful assistant reviewing a chatbot response to a user’s emotional message.

Step 1: Determine if the bot’s response is emotionally relevant and actually addresses the user’s need or question.
Step 2: If the response is vague, repetitive, or not helpful, browse the web get relevant answer rewrite it with empathy and a clear focus on what the user asked.
Step 3: Keep it under 3 sentences longer only if needed and avoid generic reassurance unless it fits the context.

User Message:
{user_input}

Bot's Original Response:
{bot_response}

Final (Validated or Improved) Response:
"""
)


from langchain.chains import LLMChain, SequentialChain

summary_chain = LLMChain(llm=gemini_llm1, prompt=summary_prompt, output_key="summarized_question")
answer_chain = LLMChain(llm=gemini_llm1, prompt=answer_prompt, output_key="gemini_response")
validate_chain = LLMChain(
    llm=gemini_llm1,
    prompt=validate_or_rewrite_prompt,
    output_key="final_response"
)

chatbot_chain = SequentialChain(
    chains=[summary_chain, answer_chain, validate_chain],
    input_variables=["user_question"],
    output_variables=["gemini_response"],
    memory=memory,
    verbose=True
)

class MentalHealthChatbot:
    def __init__(self):
        self.chain = chatbot_chain

    from embeddings import retriever

class MentalHealthChatbot:
    def __init__(self):
        self.chain = chatbot_chain

    def get_response(self, user_input):
        if not is_safe_input(user_input):
            return "I'm really sorry you're feeling this way. Please consider reaching out to a professional or a trusted person for support."

        # 🧠 Use retriever to fetch relevant content
        docs = retriever.invoke(user_input)

        context = "\n".join([doc.page_content for doc in docs])

        # 💡 You can use context to improve LLM response
        full_input = f"{user_input}\n\nRelevant Info:\n{context}"

        # Run the chain
        response = self.chain.run({"user_question": full_input})
        return response

