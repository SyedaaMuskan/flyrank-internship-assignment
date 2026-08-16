# Task CRUD API with SQLite

A simple CRUD API built with **Python, FastAPI, and SQLite**.

This project replaces the in-memory task list from the previous assignment with a persistent SQLite database.

## Features

* Create, read, update, and delete tasks
* SQLite database with automatic table creation
* Data persists after server restarts
* Input validation and proper HTTP status codes
* Interactive Swagger API documentation

## Database

The application uses a SQLite database named `tasks.db`.

The `tasks` table contains:

* `id` — integer primary key
* `title` — task title
* `done` — completion status

The database and table are created automatically when the application starts. Example tasks are inserted only when the table is empty.

## API Endpoints

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/tasks`      | Get all tasks       |
| GET    | `/tasks/{id}` | Get a specific task |
| POST   | `/tasks`      | Create a task       |
| PUT    | `/tasks/{id}` | Update a task       |
| DELETE | `/tasks/{id}` | Delete a task       |

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## SQL Example

```sql
SELECT * FROM tasks;
```

## Key Learning

The main lesson is separating the **API layer** from the **storage layer**.

```text
Client → FastAPI → SQLite
```

The API remains the same, while the storage changes from an in-memory Python list to a persistent database.
