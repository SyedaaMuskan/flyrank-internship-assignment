from fastapi import FastAPI,HTTPException,Header,Depends
import os 
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
port = os.getenv("PORT", 8000)

supabase: Client = create_client(supabase_url, supabase_key)
app = FastAPI()
def get_current_user(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = authorization.split(" ", 1)[1]

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return response.user

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
@app.get("/public/info")
def get_public_info():
    return {"message": "Welcome stranger! This info is public."}
    
@app.get("/protected/profile")
def get_profile(user=Depends(get_current_user)):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@app.get("/protected/dashboard")
def get_dashboard(user=Depends(get_current_user)):
    return {"message": f"Welcome to your dashboard, {user.email}!"}


@app.post("/auth/logout", status_code=204)
def logout(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    token = authorization.split(" ", 1)[1]

    try:
        supabase.auth.sign_out()
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return None