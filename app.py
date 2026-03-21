from fastapi import FastAPI, Query, Form, Response, Cookie, HTTPException, status
from models import UserCreate
from data import sample_products, users_db
from uuid import uuid4

app = FastAPI()

# task 3.1
@app.post('/create_user')
def create_user(user : UserCreate):
    return user

# task 3.2
@app.get('/product/{product_id}')
def get_product_by_id(product_id : int):
    for product in sample_products:
        if product['product_id'] == product_id:
            return product

@app.get('/products/search')
def search_products(keyword : str, category : str = Query(default=None), limit : int = Query(default=10, ge=0)):
    res = []
    for product in sample_products:
        if len(res) < limit and keyword in product['name'] and (not category or product['category'] == category):
            res.append(product)
    return res

# task 5.1
@app.post("/login")
def login(response : Response, username : str = Form(...), password : str = Form(...)):
    for user in users_db:
        if user.get("username") == username and user.get("password") == password:
            response.set_cookie(key="session_cookie", value=user.get("user_id"), httponly=True)
            return {"session_cookie" : user.get("user_id")}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

@app.get("/user")
async def get_user(session_cookie = Cookie()):
    for user in users_db:
        if str(user.get("user_id")) == session_cookie:
            return {"username": user.get("username")}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")