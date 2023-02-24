from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError


app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
ALGORITHM = "HS256"
crypt = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_DURATION = 1 # minute
# SECRET: terminal: openssl rand -hex 32
SECRET = "2abeb9a2142d758ac12c0112c833129d501fd9399ec7ae960fb6dcf4b61f06fd"


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str



BCRYPT_HASH = "$2a$12$sqEbY9XEnx6NgU8WYfBOxudNoQUVNUno0uZfsIyu4NyhZ8x9sLkxm" # 123
users_db = {
    "mauri1": {
        "username": "mauri1",
        "full_name": "Mauri",
        "email": "mauri123@asd.com",
        "disabled": False,
        "password": BCRYPT_HASH
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

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de auth invalidas.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if not username:
            exception.detail += " username None "
            raise exception
    except JWTError:
        exception.detail += " JWTError "
        raise exception

    # Here all is ok: we have the username
    return search_user(username)    

async def current_user(user: User = Depends(auth_user)):
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
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Password incorrecta")
    
    access_token = {
            "sub": user.username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    return { "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}
       

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True, workers=1)

# 1: POST http://127.0.0.1:8000/login Body Form username: mauri1 password:123
# 2: copy access_token from response y the next request
# 3: GET http://127.0.0.1:8000/users/me Auth Bearer mauri1
