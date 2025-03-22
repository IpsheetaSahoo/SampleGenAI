
import os
import google.generativeai as genai
import streamlit as st
import requests

from dotenv import load_dotenv

# Load .env file
load_dotenv("C:/Users/Ipsheeta/Documents/GitHub/SampleGenAI/Practice Projects/secret.env")

# Access API keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Configure Google Gemini API
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")


# Function to fetch Google audience reviews
def fetch_google_reviews(movie_name, num_reviews=5):
    params = {
        "engine": "google",
        "q": f"{movie_name} audience reviews",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    if "organic_results" not in data:
        return []

    return [
        {
            "title": review.get("title", "No Title"),
            "snippet": review.get("snippet", "No Review Content"),
        }
        for review in data["organic_results"][:num_reviews]
    ]


# Function to analyze sentiment
def analyze_sentiment(review):
    prompt = f"""
    You are an expert linguist. Analyze the sentiment of the given customer review and classify it into:
    
    - **Positive**
    - **Neutral**
    - **Negative**

    Additionally, provide a confidence score between 0 and 1 (e.g., 0.85 means 85% confident).

    **Review:** {review}

    Return the result as:  
    Sentiment: [Positive/Neutral/Negative]  
    Confidence Score: [0.00 - 1.00]  
    """

    response = model.generate_content(prompt)
    sentiment_result = response.text.split("\n")
    
    try:
        sentiment_label = sentiment_result[0].replace("Sentiment: ", "").strip()
        confidence_score = sentiment_result[1].replace("Confidence Score: ", "").strip()
    except IndexError:
        sentiment_label = "Unknown"
        confidence_score = "N/A"

    return sentiment_label, confidence_score

# Function to summarize reviews
def summarize_reviews(reviews):
    if not reviews:
        return "No reviews available for summarization."

    all_reviews = " ".join([review["snippet"] for review in reviews])
    
    prompt = f"""
    Summarize the following movie audience reviews into **two concise lines** that capture the general sentiment:

    {all_reviews}

    **Output:**  
    """

    response = model.generate_content(prompt)
    return response.text.strip()


# Streamlit UI
st.title("Sentiment Analysis")
st.subheader("Analyze Google Reviews")

# Movie Review Analysis
movie_name = st.text_input("Enter the movie name to fetch reviews", "")

if st.button("Fetch and Analyze Google Reviews"):
    if movie_name.strip():
        reviews = fetch_google_reviews(movie_name)
        if reviews:
            st.write("### Google Reviews & Sentiment Analysis:")
            for idx, review in enumerate(reviews, 1):
                sentiment, confidence = analyze_sentiment(review["snippet"])
                st.write(f"**Review {idx}:** {review['snippet']}")
                st.write(f" Sentiment: {sentiment} |  Confidence Score: {confidence}")
                st.write("---")
            
            # Display the summary
            summary = summarize_reviews(reviews)
            st.subheader(" Summary of Reviews:")
            st.success(summary)    
            
        else:
            st.warning("No reviews found. Please check the movie name.")
    else:
        st.warning("Please enter a valid movie name.")


# Manual User Input Review Analysis
st.subheader("Analyze a Review")
user_review = st.text_area("Enter your review", "")

if st.button("Analyze Sentiment"):
    if user_review.strip():
        sentiment, confidence = analyze_sentiment(user_review)
        st.success(f" Sentiment: {sentiment} |  Confidence Score: {confidence}")
    else:
        st.warning("Please enter a review to analyze.")
