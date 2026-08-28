from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

from supabase import create_client, Client
from dotenv import load_dotenv


# -----------------------------
# Load environment variables
# -----------------------------

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")


# -----------------------------
# Create Supabase client
# -----------------------------

supabase: Client = create_client(
    supabase_url,
    supabase_key
)


# -----------------------------
# Create FastAPI app
# -----------------------------

app = FastAPI()


# -----------------------------
# Security
# -----------------------------

security = HTTPBearer()


# -----------------------------
# Authentication Dependency
# -----------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Get the actual JWT token
    token = credentials.credentials

    # Verify token with Supabase
    try:
        response = supabase.auth.get_user(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # Make sure a user was returned
    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return response.user


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def read_root():
    return {
        "message": "Hello, World!"
    }


# -----------------------------
# Signup
# -----------------------------

@app.post("/auth/signup", status_code=201)
def signup(data: dict):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        print("SIGNUP RESPONSE:", response)

    except Exception as e:
        print("SIGNUP ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if response.user is None:
        raise HTTPException(
            status_code=400,
            detail="Signup failed"
        )

    return {
        "user": response.user.model_dump()
    }


# -----------------------------
# Login
# -----------------------------

@app.post("/auth/login")
def login(data: dict):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

    if response.session is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }


# -----------------------------
# Public Route
# -----------------------------

@app.get("/public/info")
def get_public_info():

    return {
        "message": "Welcome stranger! This info is public."
    }


# -----------------------------
# Protected Profile
# -----------------------------

@app.get("/protected/profile")
def get_profile(
    user=Depends(get_current_user)
):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


# -----------------------------
# Protected Dashboard
# -----------------------------

@app.get("/protected/dashboard")
def get_dashboard(
    user=Depends(get_current_user)
):

    return {
        "message": f"Welcome to your dashboard, {user.email}!",
        "user_id": user.id
    }


# -----------------------------
# Logout
# -----------------------------

@app.post("/auth/logout", status_code=204)
def logout(
    user=Depends(get_current_user)
):

    try:
        supabase.auth.sign_out()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Logout failed"
        )

    return None