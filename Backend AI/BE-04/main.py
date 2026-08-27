from fastapi import FastAPI 
import os 
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
port = os.getenv("PORT", 8000)

supabase: Client = create_client(supabase_url, supabase_key)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
    