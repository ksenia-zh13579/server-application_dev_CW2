from fastapi import FastAPI, Query, Form, Response, Cookie, HTTPException, status
from models import UserCreate
from data import sample_products, users_db
from uuid import uuid4
from itsdangerous import URLSafeTimedSerializer, BadSignature

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

# task 5.1 - 5.2
SECRET_KEY = "superduperultrasecretkey"

@app.post("/login")
def login(response : Response, username : str = Form(...), password : str = Form(...)):
    for user in users_db:
        if user.get("username") == username and user.get("password") == password:
            token_serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
            confirmation_token = token_serializer.dumps(user.get("user_id"))
            response.set_cookie(key="session_cookie", value=confirmation_token, httponly=True, max_age=60)
            return {"session_cookie" : confirmation_token}
    response.status_code = 401
    return {"message": "Unauthorized"}

@app.get("/user")
async def get_user(response: Response, session_cookie : str | None = Cookie(default=None)):
    for user in users_db:
        token_serializer = URLSafeTimedSerializer(secret_key=SECRET_KEY)
        try:
            data = token_serializer.loads(session_cookie, max_age=60)
            if user.get("user_id") == data:
                return {"username": user.get("username")}
        except:
            response.status_code = 401
            return {"message": "Unauthorized"}
    response.status_code = 401
    return {"message": "Unauthorized"}