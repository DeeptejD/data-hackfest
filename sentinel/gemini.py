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

    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()

# generates fun descriptions for each of the chracteristics of the neo
def generate_fun_descriptions(neo):
    prompt = f"""
You are Quackstronaut, a friendly space duck character talking to kids aged 8-12. Generate 4 SHORT, fun, and humorous descriptions (each max 15 words) for this asteroid's features:

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

    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    
    descriptions = {}
    for line in response.text.strip().split('\n'):
        if ':' in line:
            key, desc = line.split(':', 1)
            descriptions[key.strip().lower()] = desc.strip()
    
    return descriptions


def chat_with_quackstronaut(neo, question):
    prompt = f"""
You are Quackstronaut, a friendly, enthusiastic space duck companion for kids aged 8-12. You're helping them learn about this specific asteroid:

Asteroid: {neo['name']}
Size: {neo['diameter']} meters
Speed: {neo['speed']} km/s
Distance: {neo['miss_distance']} lunar distances  
Date: {neo['date']}

A kid asks: "{question}"

Respond as Quackstronaut in a fun, encouraging way. Keep it:
- Under 100 words
- Simple language for kids
- Educational but entertaining
- Use "I'm Quackstronaut!" personality
- Include fun space facts when relevant
- Always stay positive and excited about space

If the question isn't about this asteroid or space, gently redirect to the asteroid topic.
"""

    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip()


def generate_daily_briefing(user_name, current_neos):
    # Get today's date
    from datetime import date
    today = date.today().strftime("%B %d, %Y")
    
    # Prepare NEO information for the briefing
    neo_info = ""
    if current_neos and len(current_neos) > 0:
        # Pick the most interesting NEOs (largest, closest, or fastest)
        interesting_neos = sorted(current_neos, key=lambda x: float(x.get('diameter', '0')), reverse=True)[:3]
        neo_info = "\n".join([f"- {neo['name']}: {neo['diameter']}m wide, flying by at {neo['speed']} km/s on {neo['date']}" 
                             for neo in interesting_neos])
    else:
        neo_info = "- No significant asteroids visiting today, but the cosmos is always full of surprises!"
    
    prompt = f"""
You are Quackstronaut, the most enthusiastic space duck in the galaxy! Generate a personalized daily space briefing for {user_name} on {today}.

Today's NEO Activity:
{neo_info}

Create a fun, engaging daily briefing in BULLET POINT format that includes:
1. A personalized greeting for {user_name}
2. Exciting commentary about today's space visitors (or general space facts if no NEOs)
3. A fun space fact or cosmic trivia
4. An encouraging message to explore more

Requirements:
- Keep it under 120 words total
- Use Quackstronaut's friendly, excited personality
- Format as bullet points using ONLY EMOJIS as bullet markers (no • symbols)
- Make it feel personal and special for {user_name}
- Include space puns or duck references when appropriate
- End with motivation to use CosmoDex today
- Use emojis strategically as both bullet points and content enhancement

Format example:
🦆 Quack quack, {user_name}! Ready for today's cosmic adventure?
🚀 [Space news/NEO info]
⭐ Fun fact: [Interesting space trivia]
🔭 [Encouraging exploration message]

Write it as if Quackstronaut is personally talking to {user_name} in the space lab!
"""

    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip()
