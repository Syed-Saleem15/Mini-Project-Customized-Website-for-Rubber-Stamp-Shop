from app import db  # This imports the db object from your app.py file

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(200), nullable=True)  # Image path
    rating = db.Column(db.Float, nullable=True)  # Rating column added
    
    def __repr__(self):
        return f'<Product {self.name}>'

