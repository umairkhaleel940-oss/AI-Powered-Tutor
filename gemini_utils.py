# gemini_utils.py

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# The client automatically picks up the API key from the environment
# variable GEMINI_API_KEY thanks to load_dotenv() and os.getenv().
# You must have your API key set in the .env file.
try:
    client = genai.Client()
except Exception as e:
    # A generic error message for API key issues
    print(f"Error initializing Gemini client: {e}")
    client = None

# System Instruction to define the AI's person
TUTOR_SYSTEM_INSTRUCTION = (
    "You are an expert AI Tutor. Your primary goal is to provide clear, "
    "concise, and accurate explanations for technical topics like LLMs, "
    "NLP, and Python. Always encourage learning. When asked 'what is LLM?', "
    "provide a comprehensive, beginner-friendly answer."
)

def get_gemini_response(prompt: str) -> str:
    """
    Fetches a response from the Gemini 2.5 Flash model.

    Args:
        prompt: The user's input/question.

    Returns:
        The generated text response or an error message.
    """
    if client is None:
        return "ERROR: Gemini API key is not configured correctly. Please check your .env file."

    # Use a configured chat session to maintain conversation history
    # The session_state management for chat history is typically done in Streamlit (app.py)
    # but for a single Q&A, we can use generate_content with system instructions.
    
    config = types.GenerateContentConfig(
        system_instruction=TUTOR_SYSTEM_INSTRUCTION
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config,
        )
        return response.text
    except Exception as e:
        return f"An error occurred while calling the Gemini API: {e}"

# Example of a chat function for conversational history (optional, but good practice)
def get_chat_session(history=None):
    """Initializes and returns a chat session with the tutor's person."""
    if client is None:
        return None
    
    config = types.GenerateContentConfig(
        system_instruction=TUTOR_SYSTEM_INSTRUCTION
    )

    chat = client.chats.create(
        model='gemini-2.5-flash',
        history=history if history is not None else [],
        config=config
    )
    return chat