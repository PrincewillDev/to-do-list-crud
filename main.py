from fastapi import FastAPI
from fastapi.responses import JSONResponse
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