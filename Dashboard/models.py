from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from Dashboard import app
from flask_msearch import Search

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
search = Search()
search.init_app(app)

class Customer(db.Model):
    __tablename__ = 'customer'
    __searchable__ = ['name', 'address']

    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f"ID: {self.id} Date: {self.date_added} Name: {self.name} Address: {self.address} Phone: {self.phone} Email: {self.email}"
    
class Order(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    order_sheet = db.Column(db.String(300), nullable=False)
    
    def __repr__(self):
        return f"ID: {self.id} Customer ID: {self.customer_id} Path: {self.order_sheet} Date: {self.date_added}"