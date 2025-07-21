import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
try:
    response = genai.generate_text(model="models/gemini-1.5-flash-latest", prompt="Hello from Gemini 2.0 Flash!")
    print("SUCCESS:")
    print(response.result)
except Exception as e:
    print("ERROR:")
    print(e) 