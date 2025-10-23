import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from models import (
    User,
    Product,
    User_Pydantic,
    UserIn_Pydantic,
    Product_Pydantic,
    ProductIn_Pydantic,
)
from backend.authentication import hash_password, verify_password, create_access_token, decode_access_token

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://:memory:")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app = FastAPI(title="ShopWise - Minimal E-commerce Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class TokenIn(BaseModel):
    username: str
    password: str


async def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing credentials")
    token = auth.split(" ", 1)[1].strip()
    payload = decode_access_token(token)
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin" and user.role != "admin":  
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user

@app.post("/api/auth/register", status_code=201)
async def register(payload: RegisterIn):
 
    existing = await User.filter(email=payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing2 = await User.filter(username=payload.username).first()
    if existing2:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed = hash_password(payload.password)
    user = await User.create(email=payload.email, username=payload.username, hashed_password=hashed)
    return {"status": "ok", "user": user.to_public()}

@app.post("/api/auth/login")
async def login(payload: TokenIn):
    
    user = await User.filter(username=payload.username).first()
    if not user:
        user = await User.filter(email=payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"id": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer", "user": user.to_public()}

@app.get("/api/auth/me")
async def me(user: User = Depends(get_current_user)):
    return {"user": user.to_public()}

@app.post("/api/products", status_code=201)
async def create_product(payload: ProductIn_Pydantic, user: User = Depends(get_current_user)):
 
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create products")
    product_obj = await Product.create(**payload.dict(exclude_unset=True), owner_id=user.id)
    product = await Product_Pydantic.from_tortoise_orm(product_obj)
    return {"product": product}

@app.get("/api/products", response_model=List[Product_Pydantic])
async def list_products():
    return await Product_Pydantic.from_queryset(Product.all().limit(100))

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    try:
        product = await Product.get(id=product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    return await Product_Pydantic.from_tortoise_orm(product)

@app.put("/api/products/{product_id}")
async def update_product(product_id: str, payload: ProductIn_Pydantic, user: User = Depends(get_current_user)):
    try:
        product = await Product.get(id=product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
 
    if user.role != "admin" and str(product.owner_id) != str(user.id):
        raise HTTPException(status_code=403, detail="Forbidden")
    await product.update_from_dict(payload.dict(exclude_unset=True))
    await product.save()
    return await Product_Pydantic.from_tortoise_orm(product)

@app.delete("/api/products/{product_id}", status_code=204)
async def delete_product(product_id: str, user: User = Depends(get_current_user)):
    try:
        product = await Product.get(id=product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    if user.role != "admin" and str(product.owner_id) != str(user.id):
        raise HTTPException(status_code=403, detail="Forbidden")
    await product.delete()
    return {"ok": True}


register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL", DATABASE_URL),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)