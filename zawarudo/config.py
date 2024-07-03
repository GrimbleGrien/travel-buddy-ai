import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
task = "text-generation"
