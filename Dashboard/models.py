from datetime import datetime
from Dashboard import db, search, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=False)


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
