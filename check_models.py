import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = genai.list_models()

for m in models:
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
