import streamlit as st
from chatbot_core import generate_response, memory
import time
import streamlit.components.v1 as components

# page configuration
st.set_page_config(page_title="SolaceBot", page_icon="💬")

# Title
st.title("💬 SolaceBot – Your Emotional Well Being Assistant")

# CSS for chat and background ---
st.markdown("""
    <style>

    .stApp {
        background-color: #F3F0FF;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .chat-bubble-user {
        background-color: #DCF1FF;
        color: #000;
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        border: 1px solid #d0e7f9;
        align-self: flex-end; /* Right-align user messages */
    }
    .chat-bubble-assistant {
        background-color: #FFF5E1;
        color: #000;
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
        border: 1px solid #ffe8b0;
        align-self: flex-start; /* Left-align assistant messages */
    }

    </style>
""", unsafe_allow_html=True)

components.html("""
    <script>
    const chatEnd = document.getElementById("chat-end");
    if (chatEnd) {
        chatEnd.scrollIntoView({ behavior: "smooth" });
    }
    </script>
    <div id="chat-end"></div>
""", height=0)

#  Initialize memory
if "memory" not in st.session_state:

    st.session_state.memory = []

#Reset conversation button 
if st.button("🔄 Reset Conversation"):

    st.session_state.memory.clear()
    st.rerun()

# Display past conversation 
for entry in st.session_state.memory:

    bubble_class = "chat-bubble-user" if entry["role"] == "user" else "chat-bubble-assistant"

    alignment = "flex-end" if entry["role"] == "user" else "flex-start"  # Right for user, left for bot

    st.markdown(
        f"<div class='{bubble_class}' style='align-self: {alignment};'>"
        f"{entry['content']}</div>",
        unsafe_allow_html=True
    )

#  new user input
user_input = st.chat_input("What's on your mind?")
if user_input:

    st.session_state.memory.append({"role": "user", "content": user_input})

    st.markdown(
        f"<div class='chat-bubble-user' style='align-self: flex-end;'>"
        f"{user_input}</div>",
        unsafe_allow_html=True
    )

    # Exit handling
    if user_input.strip().lower() in ["exit", "quit", "bye"]:

        goodbye_msg = "👋 Goodbye! You're always welcome back here anytime you need support."
        st.session_state.memory.append({"role": "assistant", "content": goodbye_msg})

        st.markdown(
            f"<div class='chat-bubble-assistant' style='align-self: flex-start;'>"
            f"{goodbye_msg}</div>",
            unsafe_allow_html=True
        )

        st.stop()

    #Typing animation with floating dots 
    typing_placeholder = st.empty()
    for i in range(4):

        dots = "." * (i % 4)

        typing_placeholder.markdown(
            f"<div style='color: gray; font-style: italic; align-self: flex-start;'>SolaceBot is typing{dots}</div>",
            unsafe_allow_html=True
        )

        time.sleep(0.5)

    typing_placeholder.empty()

    # Generate and display chatbot response

    response = generate_response(user_input)
    st.session_state.memory.append({"role": "assistant", "content": response})

    st.markdown(
        f"<div class='chat-bubble-assistant' style='align-self: flex-start;'>"
        f"{response}</div>",
        unsafe_allow_html=True
    )
