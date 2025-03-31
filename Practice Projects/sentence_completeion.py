
import os
import google.generativeai as genai
import streamlit as st

from dotenv import load_dotenv

# Load .env file
load_dotenv("secret.env") 

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

st.title("Sentence Completion")

user_input = st.text_area("Enter the sentence to be completed")

context=f"""
Dragging myself out of bed on a day that feels like a relentless grind, the brutal truth of adulting hits hard - 
a constant barrage of tests where restful nights are a rarity. Every day echoes the anxiety of long-lost board exams, seemingly from a 
different lifetime. The reminiscence of breaks filled with Maggie and coffee, once taken nonchalantly, now serves as a bitter reminder 
of the unappreciated simplicity of youth. Those moments, shared with a companion, now feel like distant dreams in the harsh reality of 
our grown-up existence. Yeah, we've grown up, and it stings.

"""
if st.button("Generate Completion"):
    prompt = f"""
    Given the context below, complete the following user-provided sentence:

    Context:
    \"\"\"{context}\"\"\"

    Sentence to be completed:
    \"\"\"{user_input}\"\"\"

    Please generate a coherent and meaningful completion.
    """

    response = model.generate_content(prompt)

    if response and response.text.strip():
        st.success(f"Generated Completion: {response.text.strip()}")
    else:
        st.error("Completion failed. Please try again.")