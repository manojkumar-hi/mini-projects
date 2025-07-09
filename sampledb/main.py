from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pymongo import MongoClient
from bson import ObjectId
from pydantic import EmailStr

app = FastAPI()

# Serve HTML files
app.mount("/html", StaticFiles(directory="html"), name="html")

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["marketdb"]
users_collection = db["users"]
products_collection = db["products"]
orders_collection = db["orders"]

# Home page
@app.get("/")
def home():
    return FileResponse("html/index.html")

# Register user
@app.post("/register")
def register_user(email: EmailStr = Form(...), password: str = Form(...), is_seller: bool = Form(False)):
    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="User already exists")
    users_collection.insert_one({
        "email": email,
        "password": password,
        "is_seller": is_seller
    })
    return {"message": "User registered successfully"}

# Login user
@app.post("/login")
def login_user(email: EmailStr = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "Login successful",
        "user_id": str(user["_id"]),
        "is_seller": user.get("is_seller", False)
    }

# Sell product
@app.post("/sell")
def sell_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    seller_email: EmailStr = Form(...)
):
    seller = users_collection.find_one({"email": seller_email, "is_seller": True})
    if not seller:
        raise HTTPException(status_code=403, detail="Seller not authorized")

    product = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "seller_email": seller_email
    }
    result = products_collection.insert_one(product)
    return {"message": "Product listed", "product_id": str(result.inserted_id)}

# Buy product
@app.post("/buy")
def buy_product(
    product_id: str = Form(...),
    buyer_email: EmailStr = Form(...),
    quantity: int = Form(...)
):
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product["quantity"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$inc": {"quantity": -quantity}}
    )

    order = {
        "product_id": product_id,
        "buyer_email": buyer_email,
        "quantity": quantity,
        "price": product["price"] * quantity
    }
    orders_collection.insert_one(order)
    return {"message": "Order placed successfully"}

# Get all products
@app.get("/products")
def get_products():
    products = list(products_collection.find())
    for p in products:
        p["_id"] = str(p["_id"])
    return products

# Get all orders
@app.get("/orders")
def get_orders():
    orders = list(orders_collection.find())
    for o in orders:
        o["_id"] = str(o["_id"])
    return orders
