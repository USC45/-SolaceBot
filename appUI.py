import streamlit as st
from chatbot import MentalHealthChatbot

# Initialize chatbot
chatbot = MentalHealthChatbot()

st.set_page_config(page_title="Mental Health Chatbot", layout="centered")
st.title("🌿 SolaceBot💬🧘‍♀️ ")
st.markdown("I'm here to support your mental well-being. Feel free to share anything. 💬")

# Initialize chat history and state
if "history" not in st.session_state:
    st.session_state.history = []
if "pending_response" not in st.session_state:
    st.session_state.pending_response = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

# Display chat history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(
            f"<div style='background-color:#f0f2f6;padding:10px;border-radius:10px'>"
            f"<strong>{sender}:</strong> {message}</div>", unsafe_allow_html=True
        )

# If there is a pending response, generate it first
if st.session_state.pending_response:
    response = chatbot.get_response(st.session_state.last_input)
    st.session_state.history.append(("Bot", response))
    st.session_state.pending_response = False
    print("\n")
    st.experimental_rerun()  # Show updated messages first

# Show input box only if bot is done replying
if not st.session_state.pending_response:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", placeholder="What's on your mind?", key="user_input")
        submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            st.session_state.history.append(("You", user_input.strip()))
            st.session_state.last_input = user_input.strip()
            st.session_state.pending_response = True
            st.rerun()

