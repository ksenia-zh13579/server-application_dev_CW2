from fastapi import FastAPI, Query
from models import UserCreate
from products_data import sample_products

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