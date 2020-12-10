from flask import Blueprint, session, send_from_directory
from flask import Flask, flash, redirect, jsonify
from flask import render_template, url_for, request
from flask_login import login_user, current_user, login_required
from werkzeug.utils import secure_filename

from Dashboard.main.forms import LoginForm
from Dashboard.models import Customer, Order, Admin
from Dashboard import db, bcrypt

import os

main = Blueprint("main", __name__)

UPLOAD_PATH = "E:\\Desktop\\Programming\\Dashboard\\Dashboard\\static\\Orders\\"
PDF_PATH = "/static/Orders/"


@main.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("Login Unsuccessful. Please check email and password")
    return render_template("login.html", form=form)


@main.route("/home", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        search = request.get_json()
        print(f"Searching for {search}")

        session["search"] = search
        return redirect(url_for("main.index"))
    else:
        search = session.get("search")
        if search == "" or search is None:
            customers = Customer.query.all()
        else:
            customers = Customer.query.msearch(
                search, fields=["address", "name"], limit=5
            ).all()
        return render_template("index.html", customers=customers, search=search)


@main.route("/customer", methods=["POST"])
@login_required
def add_customer():
    if request.method == "POST":
        form = request.form
        print("Adding Customer to database...\n")

        customer = Customer(
            name=form["name"],
            address=form["address"],
            phone=form["phone"],
            email=form["email"],
        )

        print(customer.__repr__())
        db.session.add(customer)
        db.session.commit()

    flash("New Customer Added!")
    return redirect(url_for("main.index"))


@main.route("/customer_orders/<int:customer_id>")
@login_required
def orders(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    order = Order.query.filter_by(customer_id=customer_id).all()

    return render_template("orders.html", customer=customer, orders=order)


@main.route("/customer_orders/<int:customer_id>", methods=["POST"])
@login_required
def add_order(customer_id):
    if request.method == "POST":
        pdf = request.files["order"]
        pdf.save(os.path.join(UPLOAD_PATH, secure_filename(pdf.filename)))

        order_sheet = PDF_PATH + pdf.filename
        form = request.form
        print(pdf.filename)
        print("Adding Order to database...\n")

        order = Order(
            id=form["invoice"], customer_id=customer_id, order_sheet=order_sheet
        )

        print(order.__repr__())
        db.session.add(order)
        db.session.commit()

    flash("New Order Added!")
    return redirect(url_for("main.orders", customer_id=customer_id))


@main.route("/delete_order/<int:customer_id>/<int:order_id>", methods=["POST"])
@login_required
def delete_order(customer_id, order_id):
    order = Order.query.filter_by(id=order_id).first()
    print("Deleting order: ")

    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("main.orders", customer_id=customer_id))
