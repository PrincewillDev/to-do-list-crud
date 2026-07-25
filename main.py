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

@app.put("/tasks/{id}")
def update_task(id: int, payload: dict):
    allowed_fields = {"title", "done"}

    if not payload:
        return JSONResponse(
            status_code=400,
            content={"message": "Request body is required"}
        )

    if not set(payload).issubset(allowed_fields):
        return JSONResponse(
            status_code=400,
            content={"message": "Only title and done fields are allowed"}
        )

    if "title" not in payload and "done" not in payload:
        return JSONResponse(
            status_code=400,
            content={"message": "At least one of title or done must be provided"}
        )

    if "title" in payload:
        title = payload["title"]

        if not isinstance(title, str):
            return JSONResponse(
                status_code=400,
                content={"message": "Title must be a string"}
            )

        if not title.strip():
            return JSONResponse(
                status_code=400,
                content={"message": "Title cannot be empty"}
            )

    if "done" in payload:
        done = payload["done"]

        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"message": "Done must be a boolean"}
            )

    for task in db:
        if task["id"] == id:
            if "title" in payload:
                task["title"] = payload["title"].strip()

            if "done" in payload:
                task["done"] = payload["done"]

            return task

    return JSONResponse(
        status_code=404,
        content={"message": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}")
def delete_task(id: int, status_code: int = 204):
    for task in db:
        if task["id"] == id:
            db.remove(task)
            return Response(status_code=status_code)
    return JSONResponse(
        status_code=404,
        content={"message": f"Task {id} not found"}
    )