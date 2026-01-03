from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Product, Supplier

products_bp = Blueprint("products", __name__, template_folder="../templates/products")

@products_bp.route("/")
def list_products():
    products = Product.query.order_by(Product.id.desc()).all()
    suppliers = {s.id: s.name for s in Supplier.query.all()}
    return render_template("products/list.html", products=products, suppliers=suppliers)

@products_bp.route("/create", methods=["GET", "POST"])
def create_product():
    suppliers = Supplier.query.all()
    if request.method == "POST":
        name = request.form["name"].strip()
        sku = request.form["sku"].strip()
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        supplier_id = request.form.get("supplier_id") or None
        if not name or not sku:
            flash("Name and SKU are required.", "error")
            return redirect(url_for("products.create_product"))
        p = Product(name=name, sku=sku, price=price, stock=stock, supplier_id=supplier_id)
        db.session.add(p)
        db.session.commit()
        flash("Product created.", "success")
        return redirect(url_for("products.list_products"))
    return render_template("products/create.html", suppliers=suppliers)

@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    suppliers = Supplier.query.all()
    if request.method == "POST":
        product.name = request.form["name"].strip()
        product.sku = request.form["sku"].strip()
        product.price = float(request.form["price"])
        product.stock = int(request.form["stock"])
        product.supplier_id = request.form.get("supplier_id") or None
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("products.list_products"))
    return render_template("products/edit.html", product=product, suppliers=suppliers)

@products_bp.route("/<int:id>/delete", methods=["POST"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("products.list_products"))
