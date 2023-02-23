from fastapi import FastAPI
from pydantic import BaseModel
from routers import customer, product
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(customer.router)
app.include_router(product.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Launch APP: uvicorn main:app --reload
