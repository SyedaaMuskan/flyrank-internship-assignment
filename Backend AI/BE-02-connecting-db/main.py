from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
import sqlite3
app=FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="This is a simple task manager API built with FastAPI"
)
Database="task_manager.db"
def create_table():
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL)''')
    conn.commit()
    conn.close()

create_table()


class task(BaseModel):
    title:str
    description:str

@app.get("/",summary="Api info")    
def root():
    return {"message":"Welcome to the Task Manager API"}

#read all tasks
@app.get("/tasks",summary="Get all tasks")
def get_tasks():
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows=cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "description": row[2]} for row in rows]

#read a single task
@app.get("/tasks/{task_id}", summary="Get a single task")
def get_task(task_id:int):
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute("select *from tasks where id=?",(task_id,))
    task=cursor.fetchone()
    conn.close()
    if task:
        return {"id": task[0], "title": task[1], "description": task[2]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")  


@app.post("/create_tasks",summary="Create a new task")
def create_task(task:task):
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (task.title, task.description))
    conn.commit()
    conn.close()
    return {"message":"Task created successfully"}



@app.put("/update_tasks/{task_id}",summary="update a task")
def update_task(task_id:int,task:task):
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute("UPDATE tasks SET title=?, description=? WHERE id=?", (task.title, task.description, task_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return {"message":"Task updated successfully"}

@app.delete('/delete_tasks/{task_id}',summary="Delete a task")
def delete_task(task_id:int):
    conn=sqlite3.connect(Database)
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return {"message":"Task deleted successfully"}