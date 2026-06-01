from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import db
from app.models import TodoCreate

app = FastAPI(title="Todo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/todos")
def list_todos():
    return db.list_all()


@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = db.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/api/todos", status_code=201)
def create_todo(data: TodoCreate):
    return db.create(data.model_dump())


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoCreate):
    todo = db.update(todo_id, data.model_dump())
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int):
    if not db.delete(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"ok": True}
