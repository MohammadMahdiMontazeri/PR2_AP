from . import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price_toman = db.Column(db.Integer)
    price_dollar = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total_toman = db.Column(db.Integer)
    total_dollar = db.Column(db.Integer)
    gdrive_link = db.Column(db.String(255),nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price_toman = db.Column(db.Integer)
    price_dollar = db.Column(db.Integer)
    count = db.Column(db.Integer)
    total_toman = db.Column(db.Integer)
    total_dollar = db.Column(db.Integer)
    gdrive_link = db.Column(db.String(255),nullable=False)