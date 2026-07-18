# BE-01 — Build Your First API Endpoint

## 📖 Overview

This project is the first assignment in the **FlyRank Backend AI Engineering Internship**.

The objective is to build the smallest possible backend application that exposes two JSON API endpoints, test them using a browser and `curl`, and publish the project to GitHub.

## 🎯 Learning Objectives

* Understand the HTTP request–response cycle
* Build a basic REST API using FastAPI
* Return JSON responses
* Test API endpoints with a browser and `curl`
* Become familiar with backend project structure
* Practice version control using Git and GitHub

## 🛠️ Tech Stack

* Python 3.x
* FastAPI
* Uvicorn

## 📁 Project Structure

```text
BE-01-First-API/
│
├── app/
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Installation

1. Navigate to the project directory.

```bash
cd BE-01-First-API
```

2. Install the required packages.

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📡 API Endpoints

| Method | Endpoint  | Description                              |
| ------ | --------- | ---------------------------------------- |
| GET    | `/`       | Returns a welcome message in JSON format |
| GET    | `/health` | Returns the health status of the API     |

## 🧪 Testing

### Browser

Open:

```text
http://127.0.0.1:8000/
```

or

```text
http://127.0.0.1:8000/health
```

### Swagger UI

FastAPI automatically generates interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### curl

```bash
curl http://127.0.0.1:8000/
```

```bash
curl http://127.0.0.1:8000/health
```

## ✅ Assignment Outcome

This project demonstrates the fundamentals of backend API development by creating a minimal FastAPI server that handles HTTP requests and returns JSON responses.
