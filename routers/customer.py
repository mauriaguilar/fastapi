from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/customer")

class Customer(BaseModel):
    cid: int
    name: str
    city: str

customers = [
    Customer(cid=1, name="Juan", city="Malabrigo"),
    Customer(cid=2, name="Jose", city="Reconquista"),
    Customer(cid=3, name="Jacinto", city="Vera"),
]


def get_customer(cid: int):
    if not cid:
        return customers
    try:
        return list(filter(lambda customer: customer.cid == cid, customers))
    except (StopIteration):
        return "customer not found: " + str(cid)

@router.get("/list")
async def customer_list():
    return get_customer(0)

@router.get("/")
async def customer_get1(cid: int):
    return get_customer(cid)
    # http://127.0.0.1:8000/customer/?id=1

@router.get("/{id}")
async def customer_get2(cid: int):
    if cid > 9:
        raise HTTPException(status_code=204, detail="Customer no existe")
    return get_customer(cid)
    # http://127.0.0.1:8000/customer/1
 
@router.get("/add")
async def customer_add(cid: int, name: str, city: str):
    customers.append(Customer(cid=cid, name=name, city=city))
    return {"message": "customer added."}

@router.delete("/del/{id}")
async def customer_del(cid: int):
    found = False
    for index, customer in enumerate(customers):
        if customer.cid == cid:
            del customers[index]
            found = True
            return {"message": "customer deleted."}
    if not found:
        return {"message": "customer not found."}

@router.get("/edit")
async def customer_edit():
    return {"message": "customer edited."}

# Launch APP: uvicorn api:app --reload
