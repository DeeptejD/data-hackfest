import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_asteroid(neo):
    prompt = f"""
You are a space expert. Summarize this asteroid in plain English:

Name: {neo['name']}
Estimated diameter: {neo['diameter']} meters
Relative speed: {neo['speed']} km/s
Miss distance: {neo['miss_distance']} lunar distances
Close approach date: {neo['date']}

Be concise, simple, and slightly fun.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()
