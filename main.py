from fastapi import FastAPI

app=FastAPI()

@app.get("/images")
def index():
    return {"name":"first data"}





