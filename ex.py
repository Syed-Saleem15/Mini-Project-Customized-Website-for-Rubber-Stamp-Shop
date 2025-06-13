from app import db
from models import Product

# Query the Product table
products = Product.query.all()
print(products)
