from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()
app.patients = []


@app.get("/welcome")
def hello_pandemic():
    return {"message": "Welcome welcome!"}


@app.get("/")
def hello_pandemic():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method")
def method_get():
    return {"method": "GET"}


@app.post("/method")
def method_post():
    return {"method": "POST"}


@app.put("/method")
def method_put():
    return {"method": "PUT"}


@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}


@app.post("/patient")
def receive_data(data: dict):
    app.patients.append(data)
    return {"id": len(app.patients)-1, "patient": data}


@app.get("/patient/{pk}")
def patient_info(pk: int):
    if 0 <= pk < len(app.patients):
        return app.patients[pk]
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
