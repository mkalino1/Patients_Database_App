from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_pandemic():
    return {"message": "Hello World during the coronavirus pandemic!"}
