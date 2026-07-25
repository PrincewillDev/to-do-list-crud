from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
db = [
    {
        "id": 1,
        "title": "Buy groceries",
        "done": False
    },
    {
        "id": 2,
        "title": "Clean the house",
        "done": True
    },
    {
        "id": 3,
        "title": "Finish the project",
        "done": False
    }
]

app = FastAPI(
    title= "To-Do List API",
    description= "A simple API for managing a to-do list.",
    version= "1.0.0",
)

@app.get("/")
def root():
    return { "name": "Task API", 
            "version": "1.0", 
            "endpoints": ["/tasks"] }

@app.get("/health")
def health_check():
    return { "status": "ok" }

@app.get("/tasks")
def get_tasks():
    return db

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in db:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"message": f"Task {id} not found"},)

@app.post("/tasks", status_code=201)
def create_task(task: dict):
    title = task.get("title")
    if title is None or not isinstance(title, str) or title.strip() == "":
        return JSONResponse(status_code=400, content={"message": "Title is required"})
    next_id = max(task["id"] for task in db) + 1 if db else 1

    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": task.get("done", False)
    }
    db.append(new_task)
    return new_task