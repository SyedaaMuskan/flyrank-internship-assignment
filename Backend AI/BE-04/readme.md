# BE-04 — Supabase Authentication API

A FastAPI backend implementing user authentication with **Supabase Auth**, including signup, login, JWT verification, protected routes, logout, and Swagger UI Bearer authentication.

## 🚀 Features

* User signup with email and password
* User login with Supabase Auth
* JWT access-token verification
* Protected profile endpoint
* Protected dashboard endpoint
* Reusable FastAPI authentication dependency
* Protected logout endpoint
* Swagger UI authentication with Bearer JWT
* Proper HTTP status codes for authentication failures

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **Supabase Auth**
* **PostgreSQL** — provided through Supabase
* **Pydantic/FastAPI validation**
* **Uvicorn**
* **python-dotenv**

## 📁 Project Structure

```text
BE-04/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> `.env` contains secret credentials and should never be committed to Git.

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd BE-04
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Do not commit this file.

### 5. Run the API

```bash
python -m uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 🔐 Authentication Flow

The authentication flow works as follows:

```text
Signup
  ↓
Supabase creates user
  ↓
Login
  ↓
Supabase returns access token
  ↓
Client sends:
Authorization: Bearer <access_token>
  ↓
FastAPI authentication dependency
  ↓
Supabase verifies JWT
  ↓
Authenticated user
  ↓
Protected endpoint
```

The reusable `get_current_user` dependency handles token extraction and verification before protected routes are executed.

## 📡 API Endpoints

| Method | Endpoint               | Authentication | Description                           |
| ------ | ---------------------- | -------------- | ------------------------------------- |
| GET    | `/`                    | Public         | Health/root endpoint                  |
| POST   | `/auth/signup`         | Public         | Create a new account                  |
| POST   | `/auth/login`          | Public         | Login and receive JWT tokens          |
| POST   | `/auth/logout`         | Required       | Logout the authenticated user         |
| GET    | `/public/info`         | Public         | Public information                    |
| GET    | `/protected/profile`   | Required       | Return authenticated user's profile   |
| GET    | `/protected/dashboard` | Required       | Return authenticated user's dashboard |

## 📝 Signup

### Request

```http
POST /auth/signup
```

```json
{
  "email": "your-email@example.com",
  "password": "Password123!"
}
```

### Successful response

Returns the newly created Supabase user.

## 🔑 Login

### Request

```http
POST /auth/login
```

```json
{
  "email": "your-email@example.com",
  "password": "Password123!"
}
```

### Response

```json
{
  "access_token": "your-access-token",
  "refresh_token": "your-refresh-token"
}
```

The `access_token` is used to access protected endpoints.

## 🛡️ Protected Routes

Protected endpoints require:

```http
Authorization: Bearer <access_token>
```

For example:

```http
GET /protected/profile
Authorization: Bearer eyJ...
```

The backend verifies the token using Supabase:

```python
response = supabase.auth.get_user(token)
```

Invalid or expired tokens result in:

```http
401 Unauthorized
```

## 👤 Profile

```http
GET /protected/profile
```

Returns authenticated user information:

```json
{
  "id": "user-id",
  "email": "user@example.com",
  "created_at": "..."
}
```

## 📊 Dashboard

```http
GET /protected/dashboard
```

Returns a personalized response for the authenticated user.

## 🚪 Logout

```http
POST /auth/logout
```

The endpoint is protected using the same `get_current_user` authentication dependency.

A successful logout returns:

```http
204 No Content
```

## 🔒 Swagger Authentication

FastAPI's `HTTPBearer` security scheme is used to integrate JWT authentication with Swagger UI.

Open:

```text
http://127.0.0.1:8000/docs
```

Click:

**Authorize 🔒**

Enter the Bearer access token and authorize the Swagger session.

Protected endpoints can then be tested directly from Swagger UI.

## 🧪 Authentication Tests

The following scenarios were tested:

* Public endpoint without authentication → `200 OK`
* Protected profile without authentication → `401 Unauthorized`
* Protected dashboard without authentication → `401 Unauthorized`
* Protected endpoint with invalid token → `401 Unauthorized`
* Protected profile with valid token → `200 OK`
* Protected dashboard with valid token → `200 OK`
* Logout without authentication → `401 Unauthorized`
* Logout with valid authentication → `204 No Content`

## 🔐 Security Notes

* Supabase is responsible for authentication and JWT validation.
* Access tokens should never be hard-coded in the source code.
* Supabase credentials are stored in environment variables.
* `.env` is excluded from Git using `.gitignore`.
* Protected routes use a reusable FastAPI dependency instead of duplicating authentication logic.

## 📚 What I Learned

Through this assignment, I practiced:

* Integrating Supabase Auth with FastAPI
* Creating signup and login endpoints
* Working with JWT access tokens
* Understanding Bearer authentication
* Creating reusable FastAPI dependencies
* Protecting multiple API routes
* Using HTTP status codes such as `401`, `400`, `201`, and `204`
* Configuring Swagger UI for authentication
* Testing authenticated and unauthenticated API requests
* Managing environment variables and secrets
