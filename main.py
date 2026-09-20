from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return {"message": "Hello, World!"}


products = [
    Products(
        id=1,
        name="afnan",
        description="low budget",
        price=12.200,
        quantity=3
    ),
    Products(
        id=18,
        name="afnuu",
        description="low budget",
        price=12.200,
        quantity=3
    ),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count()

    if count == 0:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products


@app.get("/product/{id}")
def get_pro_by_id(id: int, db:Session = Depends(get_db)):

    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product
    return "product is not found"

@app.post("/products")
def add_product(product: Products, db:Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return products

@app.put("/products/{id}")
def update_product(id: int, product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated"
    else:
        return "no product found"

    return "No product found"


@app.delete("/products/{id}")
def delete_product(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return "Product is not matching"