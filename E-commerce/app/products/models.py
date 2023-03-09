from app import db, app
from datetime import datetime


class Product(db.Model):
    __searchable__ = ['name', 'des']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    color = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('categories', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(30), nullable=False, unique=True)   

    def __repr__(self):
        return '<Brand %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    
    def __repr__(self):
        return '<Category %r>' % self.name


with app.app_context():
    db.create_all()