import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
# MODEL = "groq/llama3-70b-8192"
MODEL = "groq/meta-llama/llama-4-scout-17b-16e-instruct"
DEBUG = False
