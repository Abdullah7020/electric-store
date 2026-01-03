from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Customer

customers_bp = Blueprint("customers", __name__, template_folder="../templates/customers")

@customers_bp.route("/")
def list_customers():
    customers = Customer.query.order_by(Customer.id.desc()).all()
    return render_template("customers/list.html", customers=customers)

@customers_bp.route("/create", methods=["GET", "POST"])
def create_customer():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("customers.create_customer"))
        c = Customer(name=name, email=email, phone=phone, address=address)
        db.session.add(c)
        db.session.commit()
        flash("Customer created.", "success")
        return redirect(url_for("customers.list_customers"))
    return render_template("customers/create.html")

@customers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == "POST":
        customer.name = request.form["name"].strip()
        customer.email = request.form.get("email")
        customer.phone = request.form.get("phone")
        customer.address = request.form.get("address")
        db.session.commit()
        flash("Customer updated.", "success")
        return redirect(url_for("customers.list_customers"))
    return render_template("customers/edit.html", customer=customer)

@customers_bp.route("/<int:id>/delete", methods=["POST"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer deleted.", "success")
    return redirect(url_for("customers.list_customers"))
