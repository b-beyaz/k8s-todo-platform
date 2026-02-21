from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="K8s Todo API")

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

todos: List[Todo] = []

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    for t in todos:
        if t.id == todo.id:
            raise HTTPException(status_code=400, detail="Todo with this ID already exists")
    todos.append(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for t in todos:
        if t.id == todo_id:
            todos.remove(t)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")