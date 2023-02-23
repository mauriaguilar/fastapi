from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/product")

class Product(BaseModel):
    pid: int
    stock: int

products = [
    Product(pid=1, stock=3),
    Product(pid=2, stock=5),
    Product(pid=3, stock=5),
]


def get_product(pid: int):
    if not pid:
        return products
    try:
        return list(filter(lambda product: product.pid == pid, products))
    except (StopIteration):
        return "product not found: " + str(pid)

@router.get("/list")
async def product_list():
    return get_product(0)
    # http://127.0.0.1:8000/customer/

@router.get("/")
async def product_id(pid: int):
    return get_product(pid)
    # http://127.0.0.1:8000/product/?id=0
    # http://127.0.0.1:8000/product/?id=1

@router.get("/{id}")
async def product_get(id: int):
    if id > 99:
        raise HTTPException(status_code=204, detail="Product no existe")
    return get_product(id)
    # http://127.0.0.1:8000/product/1
 
@router.get("/add")
async def product_add(pid: int, stock: int):
    products.append(Product(pid=pid, stock=stock))
    return {"message": "product added."}

@router.delete("/del/{id}")
async def product_del(pid: int):
    found = False
    for index, product in enumerate(products):
        if product.pid == pid:
            del products[index]
            found = True
            return {"message": "product deleted."}
    if not found:
        return {"message": "product not found."}

@router.get("/edit")
async def customer_edit():
    return {"message": "product edited."}

# Launch APP: uvicorn api:app --reload
