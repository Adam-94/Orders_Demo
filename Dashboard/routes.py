from flask import Flask, flash, redirect, session, send_from_directory
from flask import render_template, url_for, request, jsonify

from Dashboard.forms import LoginForm
from Dashboard.models import db, Customer, Order
from Dashboard import app
from werkzeug.utils import secure_filename

import os

UPLOAD_PATH = 'E:\\Desktop\\Programming\\Dashboard\\Dashboard\\static\\Orders\\'
PDF_PATH = '/static/Orders/'

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        form = request.form
        print('Adding Customer to database...\n')

        customer = Customer(name=form['name'],
                            address=form['address'],
                            phone=form['phone'],
                            email=form['email'])

        print(customer.__repr__())
        db.session.add(customer)
        db.session.commit()
    
    flash('New Customer Added!')
    return redirect(url_for('index'))

@app.route('/customer_orders/<int:customer_id>')
def orders(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    order = Order.query.filter_by(customer_id=customer_id).all()

    return render_template('orders.html', customer=customer, orders=order)
    

@app.route('/customer_orders/<int:customer_id>', methods=['GET','POST'])
def add_order(customer_id):
    if request.method == 'POST':
        pdf = request.files['order']
        pdf.save(os.path.join(UPLOAD_PATH, secure_filename(pdf.filename)))
        
        order_sheet = PDF_PATH + pdf.filename
        form = request.form
        print(pdf.filename)
        print('Adding Order to database...\n')

        order = Order(id=form['invoice'],
                      customer_id=customer_id,
                      order_sheet=order_sheet)

        print(order.__repr__())
        db.session.add(order)
        db.session.commit()
    
    flash('New Order Added!')
    return redirect(url_for('orders', customer_id=customer_id))





