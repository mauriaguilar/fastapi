from fastapi import FastAPI
from pydantic import BaseModel
from routers import customer, product, user, auth_jwt
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(auth_jwt.router)

# Launch APP: uvicorn main:app --reload
