from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user")

class User(BaseModel):
    uid: int

users = [
    User(uid=1),
    User(uid=2),
    User(uid=3),
]

ENTITY = "User"

def get_user(uid: int):
    if not uid:
        return users
    try:
        return list(filter(lambda customer: customer.uid == uid, users))
    except (StopIteration):
        return "customer not found: " + str(uid)

@router.get("/list")
async def get1():
    return get_user(0)

@router.get("/")
async def get2(uid: int):
    return get_user(uid)

@router.get("/{id}")
async def get3(uid: int):
    if uid > 9:
        raise HTTPException(status_code=204, detail=ENTITY + " no existe")
    return get_user(uid)

@router.get("/add")
async def add(uid: int):
    users.append(User(uid=uid))
    return {"message": ENTITY + " added."}

@router.delete("/del/{id}")
async def delete(uid: int):
    found = False
    for index, customer in enumerate(users):
        if customer.uid == uid:
            del users[index]
            found = True
            return {"message": ENTITY + " deleted."}
    if not found:
        return {"message": ENTITY + " not found."}

@router.get("/edit")
async def edit():
    return {"message": ENTITY + " edited."}
