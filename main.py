from fastapi import FastAPI , HTTPException, Response, status, Depends, Cookie, Request
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from hashlib import sha256
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import secrets


app = FastAPI()
app.counter: int = 0
app.patients_storage = []
app.secret_key = 'this_is_a_secret_string'
app.tokens_storage = {}
# app.user = {'trudnY': 'PaC13Nt'}
security = HTTPBasic()

username = 'trudnY'
password = 'PaC13Nt'
templates = Jinja2Templates(directory="templates")


class Patient(BaseModel):
    name: str
    surname: str


@app.get('/welcome')
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return templates.TemplateResponse("item.html", {"request": request, "user": "trudnY"})


@app.post('/login')
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    # username, password = app.user.items()
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
def add_patient(*, response: Response, patient: Patient, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if app.counter > len(app.patients_storage):
        app.patients_storage.append(patient)
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = f"/patient/{len(app.patients_storage)-1}"
    response.status_code = status.HTTP_302_FOUND


@app.get("/patient")
def show_patients(response: Response, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return app.patients_storage


@app.get("/patients/{id}")
def show_patient(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    response.set_cookie(key="session_token", value=session_token)
    if id < len(app.patients_storage):
        return app.patients_storage[id]


@app.delete("patient/{id}")
def delete_patient(response: Response, id: int, session_token: str = Cookie(None)):
    if session_token not in app.tokens_storage:
        raise HTTPException(status_code=401, detail="Unauthorized")
    app.patients_storage.remove(id)
    response.status_code = status.HTTP_204_NO_CONTENT


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