from fastapi import FastAPI,HTTPException
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

@app.post("/auth/signup",status_code=201)
def signup(data:dict):
    email= data.get("email")
    password= data.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    response = supabase.auth.signup({"email": email, "password": password})
    if response.user is None:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"user": response.user.model_dump()}   

@app.post("/auth/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if response.session is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }    

    