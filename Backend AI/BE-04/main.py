from fastapi import FastAPI,HTTPException,Header
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
@app.get("/public/info")
def get_public_info():
    return {"message": "Welcome stranger! This info is public."}
    
@app.get("/protected/profile")
def get_profile(authorization: str = Header(None)):
    
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

    token = authorization.split(" ")[1]

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    return {
        "message": "You have access to the protected profile"
    }
@app.get("/protected/profile")
def get_profile(authorization: str = Header(None)):

    # 1. Check if Authorization header exists
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    # 2. Check that it uses Bearer format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    # 3. Extract the actual token
    token = authorization.split(" ", 1)[1]

    # 4. Make sure a token was actually provided
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    # 5. Ask Supabase to verify the token
    try:
        response = supabase.auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # 6. Make sure Supabase returned a user
    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # 7. Return authenticated user's information
    user = response.user

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }