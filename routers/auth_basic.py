from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str



users_db = {
    "mauri1": {
        "username": "mauri1",
        "full_name": "Mauri",
        "email": "mauri123@asd.com",
        "disabled": False,
        "password": "123"
    },
    "mauri2": {
        "username": "mauri2",
        "full_name": "Mauri2",
        "email": "mauri234@asd.com",
        "disabled": True,
        "password": "123"
    }
}

def search_user(username: str):
    if username in users_db:
        #return User(**users_db[username])
        return UserDB(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    
    with open("info.txt", "w+", encoding="utf-8")  as file:
        file.write(str(oauth2))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="No esta autorizado. Credenciales de auth invalidas.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="User no existe")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Password incorrecta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True, workers=1)

# 1: POST http://127.0.0.1:8000/login Body Form username: mauri1 password:123
# 2: copy access_token from response y the next request
# 3: GET http://127.0.0.1:8000/users/me Auth Bearer mauri1
