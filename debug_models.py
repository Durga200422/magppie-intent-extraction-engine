import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Checking available models for your API key...")
for model in client.models.list():
    print(f"-> {model.name}")