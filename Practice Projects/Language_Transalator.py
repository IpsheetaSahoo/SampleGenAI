import os
import google.generativeai as genai
import streamlit as st

from dotenv import load_dotenv

# Load .env file
load_dotenv("C:/Users/Ipsheeta/Documents/GitHub/SampleGenAI/Practice Projects/secret.env")

# Access API keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing or not set in the .env file.")

# Configure Google Gemini API
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
st.title("Language Translator")

languages = [
    "Hindi", "Urdu", "Spanish", "French", "German", "Russian",
    "Chinese (Simplified)", "Japanese", "Korean", "Arabic", "Portuguese", "Italian", "Dutch", "English"
]

source_lang = st.selectbox("Select source language", ["Auto-Detect (English Default)", "English"] + languages)
user_input = st.text_area("Enter text to be translated", "")
target_lang = st.selectbox("Select target language", languages)

prompt = f"""
You are an expert multilingual translator.  
Translate the following text from **{source_lang}** to **{target_lang}**  
Ensure the correct script is used.

**Text:**  
{user_input}  

**Translation (in {target_lang} script):**  
"""

if st.button("Translate"):
    if not user_input.strip():
        st.warning("Please enter text to translate.")
    else:
        response = model.generate_content(prompt)
        if response and response.text.strip():
            st.success(f"Translated text: {response.text.strip()}")
        else:
            st.error("Translation failed. Please try again.")


   