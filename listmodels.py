from dotenv import load_dotenv
import os
import google.generativeai as genai


def gemini_models():
    gemini_api_key = os.getenv("gemini_api_key")
    genai.configure(api_key=gemini_api_key)
    
    # List all the models that support the generateContent method
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

gemini_models()
