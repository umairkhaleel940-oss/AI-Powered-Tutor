# app.py

import streamlit as st
from gemini_utils import get_gemini_response # Import the backend function

# --- Streamlit Frontend Configuration ---
st.set_page_config(
    page_title="🎓 AI Tutor (Gemini API)",
    layout="centered"
)

st.title("🎓 AI Tutor")
st.markdown("Ask any technical question (e.g., 'What is LLM?' or 'Explain NLP in Python').")

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle User Input and Generate Response ---
if prompt := st.chat_input("Ask your question here..."):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call the backend function to get the Gemini response
            full_response = get_gemini_response(prompt)
        
        # Display assistant response and stream the text
        st.markdown(full_response)
        
    # 4. Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})