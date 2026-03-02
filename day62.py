from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------
# Database Setup
# -----------------------------
DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# -----------------------------
# Database Model
# -----------------------------
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

Base.metadata.create_all(bind=engine)

# -----------------------------
# Pydantic Model
# -----------------------------
class Task(BaseModel):
    title: str
    description: str

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Day 62 - FastAPI with SQLite 🚀"}

@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(TaskDB).all()
    db.close()
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    db = SessionLocal()
    new_task = TaskDB(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    db.close()
    return {"message": "Task added successfully", "task": new_task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        db.close()
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()
    db.close()
    return {"message": "Task deleted successfully"}