import os
import google.generativeai as genai
import streamlit as st

# Load API Key Securely
GEMINI_API_KEY = "AIzaSyDGcrRFpf-WM2hxKA2rFp1gLGCxpbWWjSI"

# Configure Google Gemini API
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")
st.title("Language Translator")

languages = [
    "Hindi", "Urdu", "Spanish", "French", "German", "Russian",
    "Chinese (Simplified)", "Japanese", "Korean", "Arabic", "Portuguese", "Italian", "Dutch"
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


   