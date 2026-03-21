from fastapi import FastAPI, Query, Form, Response, Cookie
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
current_user = {}

@app.post("/login")
def login(response : Response, username : str = Form(...), password : str = Form(...)):
    for user in users_db:
        if user["username"] == username and user["password"] == password:
            current_user["session_cookie"] = uuid4()
            current_user["data"] = user
            response.set_cookie(key="session_cookie", value=current_user["session_cookie"], httponly=True)
            return {"message" : "cookie has been set"}
    return {"error" : "Invalid credentials!"}

@app.get("/user")
async def get_user(session_cookie = Cookie()):
    print(type(session_cookie), type(str(current_user.get("session_cookie"))))
    if str(current_user.get("session_cookie")) == session_cookie:
        return {"user": current_user.get("data")}
    return {"message": "Unauthorized"}