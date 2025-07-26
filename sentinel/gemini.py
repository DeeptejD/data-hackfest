import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# generates a quick summary about the neo
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

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()

# generates fun descriptions for each of the chracteristics of the neo
def generate_fun_descriptions(neo):
    prompt = f"""
You are Astro, a friendly space robot character talking to kids aged 8-12. Generate 4 SHORT, fun, and humorous descriptions (each max 15 words) for this asteroid's features:

Asteroid: {neo['name']}
Size: {neo['diameter']} meters
Speed: {neo['speed']} km/s  
Distance: {neo['miss_distance']} lunar distances
Date: {neo['date']}

Create exactly 4 descriptions in this format:
SIZE: [fun description about its size]
SPEED: [fun description about its speed]  
DISTANCE: [fun description about its distance]
DATE: [fun description about its visit date]

Make them kid-friendly, funny, and use simple comparisons kids understand!
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    descriptions = {}
    for line in response.text.strip().split('\n'):
        if ':' in line:
            key, desc = line.split(':', 1)
            descriptions[key.strip().lower()] = desc.strip()
    
    return descriptions


def chat_with_astro(neo, question):
    prompt = f"""
You are Astro, a friendly, enthusiastic space robot companion for kids aged 8-12. You're helping them learn about this specific asteroid:

Asteroid: {neo['name']}
Size: {neo['diameter']} meters
Speed: {neo['speed']} km/s
Distance: {neo['miss_distance']} lunar distances  
Date: {neo['date']}

A kid asks: "{question}"

Respond as Astro in a fun, encouraging way. Keep it:
- Under 100 words
- Simple language for kids
- Educational but entertaining
- Use "I'm Astro!" personality
- Include fun space facts when relevant
- Always stay positive and excited about space

If the question isn't about this asteroid or space, gently redirect to the asteroid topic.
"""

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip()
