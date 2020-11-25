from flask import Flask, flash, redirect, session, send_from_directory
from flask import render_template, url_for, request, jsonify

from Dashboard.forms import LoginForm
from Dashboard.models import db, Customer, Order
from Dashboard import app
from werkzeug.utils import secure_filename
from flask_msearch import Search

import os

UPLOAD_PATH = 'E:\\Desktop\\Programming\\Dashboard\\Dashboard\\static\\Orders\\'
PDF_PATH = '/static/Orders/'

@app.route('/')
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
          search = request.get_json()
          print(f'Searching for {search}') 

          session['search'] = search
          return redirect(url_for('index'))
    else:
          search = session.get('search')
          if search == '' or search == None:
              customers = Customer.query.all()
          else:
              customers = Customer.query.msearch(search, fields=['address', 'name'], limit=5).all()           
          
          return render_template('index.html', customers=customers, search=search)

@app.route('/search', methods=['GET','POST'])
def search():
      if request.method == 'POST':
          search = request.get_json()
          print(f'Searching for {search}') 

          session['search'] = search
          return redirect(url_for('search'))
      else:
        search = session.get('search')
        query = Customer.query.msearch(search, fields=['address', 'name'], limit=5).all() 
        return render_template('search.html', customers=query, search=search)

      

# @app.route('/search', methods=['POST'])
# def search():
#     customer = {
#         "id": '',
#         "date": '',
#         "name": '',
#         "address": '',
#         "phone": '',
#         "email": ''
#     }

#     if request.method == 'POST':
#         search = request.get_json()

#         print(f'Search: {search}')
#         query = Customer.query.filter_by(id=search).first()
#         print(query.name)

#         customer['id'] = query.id
#         customer['date'] = query.date_added.strftime('%d-%m-%Y')
#         customer['name'] = query.name
#         customer['address'] = query.address
#         customer['phone'] = query.phone
#         customer['email'] = query.email

#         session['customer'] = customer
#         session['search'] = search

#         return jsonify(customer)

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



