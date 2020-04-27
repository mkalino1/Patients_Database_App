from fastapi import FastAPI , HTTPException, Response, status, Depends, Cookie, Request
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from hashlib import sha256
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict
import secrets

class Patient(BaseModel):
    name: str
    surname: str

app = FastAPI()
app.counter: int = 0
app.patients_storage: Dict[int, Patient] = {}
app.secret_key = 'this_is_a_secret_string'
app.tokens_storage = {}
security = HTTPBasic()

username = 'trudnY'
password = 'PaC13Nt'
templates = Jinja2Templates(directory="templates")


@app.get('/welcome')
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return templates.TemplateResponse("item.html", {"request": request, "user": "trudnY"})


@app.post('/login')
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.tokens_storage[session_token] = credentials.username
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND
    return response


@app.post('/logout')
def logout(*, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    app.tokens_storage.pop(session_token)
    response.headers["Location"] = "/"
    response.status_code = status.HTTP_302_FOUND

# ***********ZAD 5***************


@app.post("/patient")
async def add_patient(patient: Patient,response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unathorised")
    app.patients_storage[app.counter] = patient
    response.headers["Location"] = f"/patient/{app.counter}"
    response.status_code = 302
    app.counter += 1
    return response


@app.get("/patient")
def show_patients(response:Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unathorised")
    if len(app.patients_storage) == 0:
        raise HTTPException(status_code=204)
    return app.patients_storage


@app.get("/patient/{pk}")
def show_patient(pk: int, response:Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unathorised")
    if pk in app.patients_storage:
        return app.patients_storage.get(pk)
    else:
        raise HTTPException(status_code=204)


@app.delete("/patient/{pk}")
async def delete_patient(pk: int, response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unathorised")
    if pk in app.tokens_storage:
        del app.tokens_storage[pk]
        response.headers["Location"] = "/patient"
        response.status_code = 204
        return response
    else:
        raise HTTPException(status_code=204)


#********************** ZAJECIA 1 **********************************


@app.get("/")
def hello_pandemic():
    return {"message": "Hello World during the coronavirus pandemic!"}

'''
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
    app.patients_storage.append(data)
    return {"id": len(app.patients_storage) - 1, "patient": data}


@app.get("/patient/{pk}")
def patient_info(pk: int):
    if 0 <= pk < len(app.patients_storage):
        return app.patients_storage[pk]
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

'''