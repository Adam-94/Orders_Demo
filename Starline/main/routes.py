from flask import Blueprint, session
from flask import flash, redirect
from flask import render_template, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from Starline.main.forms import LoginForm
from Starline.models import Customer, Order, Admin
from Starline import db, bcrypt

import os

main = Blueprint("main", __name__)

UPLOAD_PATH = "E:\\Desktop\\Programming\\Dashboard\\Starline\\static\\Orders\\"
PDF_PATH = "/static/Orders/"


@main.route("/")
def root():
    return redirect(url_for("main.index"))


@main.route("/login", methods=["GET", "POST"])
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
    return "Login"


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))


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

        count = db.session.query(Customer).count()
        print("Adding Customer to database...\n")

        customer = Customer(
            name=form["name"],
            address=form["address"],
            phone=form["phone"],
            email=form["email"],
        )

        customer_exists = (
            db.session.query(Customer.phone).filter_by(phone=customer.phone).scalar()
            is not None
        )

        if customer_exists:
            flash("Error: Phone number is already in use!")
        elif count >= 49:
            flash("Error: Too many customers")
        else:
            print(customer.__repr__())
            db.session.add(customer)
            db.session.commit()
            flash("New Customer Added!")

    return redirect(url_for("main.index"))


@main.route("/delete_customer/<int:customer_id>", methods=["GET", "POST"])
@login_required
def delete_customer(customer_id):
    Customer.query.filter_by(id=customer_id).delete()
    Order.query.filter_by(customer_id=customer_id).delete()
    print("Deleting customer")
    db.session.commit()

    for index, customer in enumerate(Customer.query.all()):
        if customer.id != index:
            customer.id = index + 1
            db.session.commit()

    flash("Successfully Deleted Customer!")
    return redirect(url_for("main.index", customer_id=customer_id))


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
        pdf_files = []

        files = request.files.getlist("order")
        form = request.form

        order_count = db.session.query(Order).count()

        if len(files) > 1:
            for pdf in files:
                pdf.save(os.path.join(UPLOAD_PATH, secure_filename(pdf.filename)))
                pdf_files.append(PDF_PATH + pdf.filename)

            order = Order(
                id=form["invoice"],
                customer_id=customer_id,
                order_sheet1=pdf_files[0],
                order_sheet2=pdf_files[1],
            )
        else:
            pdf = request.files["order"]
            pdf.save(os.path.join(UPLOAD_PATH, secure_filename(pdf.filename)))
            pdf_files.append(PDF_PATH + pdf.filename)

            order = Order(
                id=form["invoice"], customer_id=customer_id, order_sheet1=pdf_files[0]
            )

        print(pdf_files)
        print("Adding Order to database...\n")

        if Order.query.filter_by(id=order.id).first():
            flash("Error: Invoice number already in use")
        elif order_count >= 49:
            flash("Error: Too many orders")
        else:
            print(order.__repr__())
            db.session.add(order)
            db.session.commit()
            flash("New Order Added!")
    return redirect(url_for("main.orders", customer_id=customer_id))


@main.route("/delete_order/<int:customer_id>/<int:order_id>", methods=["GET", "POST"])
@login_required
def delete_order(customer_id, order_id):
    order = Order.query.filter_by(id=order_id).first()
    print("Deleting order: ", order)

    db.session.delete(order)
    db.session.commit()
    flash("Successfully Deleted Order!")
    return redirect(url_for("main.orders", customer_id=customer_id))
