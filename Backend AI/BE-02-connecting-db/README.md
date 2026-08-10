# Task CRUD API with SQLite

A simple REST API built with **Python, FastAPI, and SQLite** for managing tasks.

This project is the continuation of the first CRUD API assignment. In the previous version, tasks were stored in an in-memory Python list, which meant all data disappeared whenever the server restarted.

In this version, the in-memory storage has been replaced with a **SQLite database**, while keeping the API endpoints and their behavior the same.

## What I Learned

The main idea of this assignment is the separation between the **API layer** and the **data layer**.

### Previous architecture

```text
Client → FastAPI → Python List
```

### Current architecture

```text
Client → FastAPI → SQLite Database
```

The client still uses the same API endpoints. Only the way data is stored has changed.

This demonstrates an important backend principle:

> The API describes what the application does, while the database describes where the data is stored.

## Features

* Create tasks
* Read all tasks
* Read a single task
* Update tasks
* Delete tasks
* Validate task titles
* Return appropriate HTTP status codes
* Automatically create the SQLite database
* Automatically create the `tasks` table
* Insert example tasks only when the table is empty
* Persist data across server restarts
* Explore and modify data using SQL

## Technology Stack

* **Python**
* **FastAPI**
* **SQLite**
* **sqlite3**
* **Uvicorn**

SQLite is used because it is lightweight and does not require a separate database server.

## Project Structure

```text
task-crud-api/
│
├── main.py
├── tasks.db
├── requirements.txt
└── README.md
```

### `main.py`

Contains the FastAPI application, API endpoints, database initialization, validation, and CRUD operations.

### `tasks.db`

The SQLite database file where tasks are stored persistently.

### `requirements.txt`

Contains the Python dependencies required to run the application.

## Database Structure

The application automatically creates a database called:

```text
tasks.db
```

Inside it, there is a table called:

```text
tasks
```

The table contains:

| Column  | Type    | Purpose                |
| ------- | ------- | ---------------------- |
| `id`    | INTEGER | Unique task identifier |
| `title` | TEXT    | Task title             |
| `done`  | BOOLEAN | Completion status      |

The table is created automatically if it does not already exist.

Three example tasks are inserted only when the table is empty.

## API Endpoints

| Method | Endpoint      | Purpose         |
| ------ | ------------- | --------------- |
| GET    | `/`           | API information |
| GET    | `/health`     | Health check    |
| GET    | `/tasks`      | Get all tasks   |
| GET    | `/tasks/{id}` | Get one task    |
| POST   | `/tasks`      | Create a task   |
| PUT    | `/tasks/{id}` | Update a task   |
| DELETE | `/tasks/{id}` | Delete a task   |

## CRUD Operations

### Create

```http
POST /tasks
```

Example request:

```json
{
  "title": "Learn SQLite"
}
```

A successful creation returns:

```text
201 Created
```

and the newly created task.

### Read

```http
GET /tasks
```

Returns all tasks stored in the database.

To retrieve one task:

```http
GET /tasks/1
```

If the task does not exist, the API returns:

```text
404 Not Found
```

### Update

```http
PUT /tasks/1
```

Example:

```json
{
  "title": "Learn SQLite deeply",
  "done": true
}
```

### Delete

```http
DELETE /tasks/1
```

A successful deletion returns:

```text
204 No Content
```

## Validation

A task must have a non-empty title.

For example:

```json
{
  "title": ""
}
```

is rejected with:

```text
400 Bad Request
```

This validation is part of the application's business logic and remains unchanged from the previous in-memory version.

## Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd task-crud-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the server

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

From Swagger UI, all CRUD endpoints can be tested directly.

## Example SQL Queries

The database can also be opened using a SQLite database viewer such as DB Browser for SQLite.

### List all tasks

```sql
SELECT * FROM tasks;
```

### Show completed tasks

```sql
SELECT * FROM tasks WHERE done = 1;
```

### Count tasks

```sql
SELECT COUNT(*) FROM tasks;
```

### Mark all tasks as completed

```sql
UPDATE tasks SET done = 1;
```

### Delete completed tasks

```sql
DELETE FROM tasks WHERE done = 1;
```

Changes made directly in SQLite can be observed through the API.

## Persistence Test

One of the main goals of this assignment is to demonstrate persistence.

### Before SQLite

```text
Start server
    ↓
Create task
    ↓
Stop server
    ↓
Start server
    ↓
Task is gone
```

### With SQLite

```text
Start server
    ↓
Create task
    ↓
Stop server
    ↓
Start server
    ↓
Task is still there
```

The data survives because it is stored in `tasks.db` rather than only in the application's memory.

## Key Takeaway

The most important lesson from this assignment was not simply learning SQLite.

It was understanding that the **API and the storage layer can be changed independently**.

The API remains:

```text
GET
POST
PUT
DELETE
```

while the storage implementation changes from:

```text
Python List
```

to:

```text
SQLite
```

This separation makes it easier to move to other databases such as PostgreSQL or MySQL in the future without changing how clients interact with the API.

## Assignment Checkpoints

* [x] SQLite database created automatically
* [x] `tasks` table created automatically
* [x] Three example tasks inserted only when the table is empty
* [x] Tasks stored in SQLite instead of an in-memory list
* [x] GET endpoints read from the database
* [x] POST inserts tasks into the database
* [x] PUT updates database records
* [x] DELETE removes database records
* [x] Data survives server restarts
* [x] Unknown task IDs return 404
* [x] Invalid task titles return 400
* [x] Swagger documentation available
* [x] Database can be inspected using SQLite tools
