from fastapi import FastAPI

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