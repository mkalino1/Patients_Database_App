from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_pandemic():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method")
def read_item():
    return {"method": "GET"}


@app.post("/method")
def read_item():
    return {"method": "POST"}


@app.put("/method")
def read_item():
    return {"method": "PUT"}


@app.delete("/method")
def read_item():
    return {"method": "DELETE"}
