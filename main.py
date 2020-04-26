from fastapi import FastAPI , HTTPException, Response, status, Depends, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from hashlib import sha256
import secrets


app = FastAPI()
app.counter: int = 0
app.token_counter: int = 0
app.patients_storage = []
app.secret_key = 'this_is_a_secret_string'
app.tokens_storage = {}
# app.user = {'trudnY': 'PaC13Nt'}
security = HTTPBasic()

username = 'trudnY'
password = 'PaC13Nt'

@app.get("/welcome")
def hello_welcome():
    return {"message": "Welcome welcome!"}


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


#********************** ZAJECIA 1 ******************

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
    app.patients_storage.append(data)
    return {"id": len(app.patients_storage) - 1, "patient": data}


@app.get("/patient/{pk}")
def patient_info(pk: int):
    if 0 <= pk < len(app.patients_storage):
        return app.patients_storage[pk]
    else:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
