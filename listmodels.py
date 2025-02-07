from dotenv import load_dotenv
import os
import google.generativeai as genai
from openai import OpenAI
import os

def gemini_models():
    gemini_api_key = os.getenv("gemini_api_key")
    genai.configure(api_key=gemini_api_key)
    
    # List all the models that support the generateContent method
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

def openai_models():
    
    openai_api_key = os.getenv('open_ai_api_key')
    client = OpenAI(api_key=openai_api_key)
    models = client.models.list()
    for model in models:
        print(model.id)

load_dotenv()
openai_models()
#gemini_models()