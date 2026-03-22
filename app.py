from fastapi import FastAPI, Query, Form, Response, Cookie, HTTPException, status
from models import UserCreate
from data import sample_products, users_db
from uuid import uuid4
from itsdangerous import TimedSerializer, BadSignature, SignatureExpired
from datetime import datetime, timezone

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

# task 5.1 - 5.3
SECRET_KEY = "superduperultrasecretkey"

@app.post("/login")
def login(response : Response, username : str = Form(...), password : str = Form(...)):
    for user in users_db:
        if user.get("username") == username and user.get("password") == password:
            timed_serializer = TimedSerializer(secret_key=SECRET_KEY)
            session_cookie = timed_serializer.dumps(user.get("user_id"))
            response.set_cookie(key="session_cookie", value=session_cookie, httponly=True, max_age=300)
            return {"session_cookie" : session_cookie}
        
    response.status_code = 401
    return {"message": "Invalid credentials"}

@app.get("/profile")
async def get_user(response: Response, session_cookie : str | None = Cookie(default=None)):
    timed_serializer = TimedSerializer(secret_key=SECRET_KEY)
    try:
        [data, time] = timed_serializer.loads(session_cookie, return_timestamp=True, max_age=300)
        timedelta = datetime.now(tz=timezone.utc) - time
        print(timedelta.seconds)

        if timedelta.seconds >= 180:
            session_cookie = timed_serializer.dumps(data)
            response.set_cookie(key="session_cookie", value=session_cookie, httponly=True, max_age=300)

        for user in users_db:
            if user.get("user_id") == data:
                return {"username": user.get("username")}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except SignatureExpired:
        response.status_code = 401
        return {"message": "Session expired"}
    except BadSignature:
        response.status_code = 401
        return {"message": "Invalid session"}
    except HTTPException as httpexp:
        response.status_code = 401
        return {"message": httpexp.detail}
    except:
        response.status_code = 401
        return {"message": "Unauthorized"}