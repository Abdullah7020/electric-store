from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Supplier

suppliers_bp = Blueprint("suppliers", __name__, template_folder="../templates/suppliers")

@suppliers_bp.route("/")
def list_suppliers():
    suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
    return render_template("suppliers/list.html", suppliers=suppliers)

@suppliers_bp.route("/create", methods=["GET", "POST"])
def create_supplier():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form.get("contact_email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        if not name:
            flash("Name is required.", "error")
            return redirect(url_for("suppliers.create_supplier"))
        s = Supplier(name=name, contact_email=email, phone=phone, address=address)
        db.session.add(s)
        db.session.commit()
        flash("Supplier created.", "success")
        return redirect(url_for("suppliers.list_suppliers"))
    return render_template("suppliers/create.html")

@suppliers_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == "POST":
        supplier.name = request.form["name"].strip()
        supplier.contact_email = request.form.get("contact_email")
        supplier.phone = request.form.get("phone")
        supplier.address = request.form.get("address")
        db.session.commit()
        flash("Supplier updated.", "success")
        return redirect(url_for("suppliers.list_suppliers"))
    return render_template("suppliers/edit.html", supplier=supplier)

@suppliers_bp.route("/<int:id>/delete", methods=["POST"])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash("Supplier deleted.", "success")
    return redirect(url_for("suppliers.list_suppliers"))
