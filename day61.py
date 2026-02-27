from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------------------
# Fake Database (In-Memory)
# -----------------------------
tasks = []

# -----------------------------
# Data Model
# -----------------------------
class Task(BaseModel):
    title: str
    description: str

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"message": "Welcome to Day 61 - FastAPI Backend 🚀"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task)
    return {"message": "Task added successfully", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if 0 <= task_id < len(tasks):
        removed = tasks.pop(task_id)
        return {"message": "Task removed", "task": removed}
    return {"error": "Invalid task ID"}