from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, current_app
from models import db, Sale, Product, Customer
from datetime import datetime
from utils.export import export_sales as export_sales_file
import qrcode, os

sales_bp = Blueprint("sales", __name__, template_folder="../templates/sales")

# List all sales
@sales_bp.route("/")
def list_sales():
    sales = Sale.query.order_by(Sale.id.desc()).all()
    return render_template("sales/list.html", sales=sales)


@sales_bp.route("/create", methods=["GET", "POST"])
def create_sale():
    products = Product.query.all()
    customers = Customer.query.all()
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        customer_id = int(request.form["customer_id"])
        quantity = int(request.form["quantity"])
        product = Product.query.get_or_404(product_id)

        # ✅ GST calculation
        GST_RATE = 0.18
        subtotal = round(product.price * quantity, 2)
        gst_amount = round(subtotal * GST_RATE, 2)
        grand_total = round(subtotal + gst_amount, 2)

        if product.stock < quantity:
            flash("Not enough stock.", "error")
            return redirect(url_for("sales.create_sale"))

        # 👉 Generate custom sale code
        year = datetime.utcnow().year
        last_sale = Sale.query.order_by(Sale.id.desc()).first()
        next_number = (last_sale.id + 1) if last_sale else 1
        sale_code = f"{year}-NO-{next_number:03d}"

        # ✅ Save Sale with GST included
        sale = Sale(
            sale_code=sale_code,
            product_id=product_id,
            customer_id=customer_id,
            quantity=quantity,
            total=grand_total,   # includes GST
            gst=gst_amount       # stored separately
        )

        # Reduce stock
        product.stock -= quantity

        db.session.add(sale)
        db.session.commit()

        # ✅ Generate QR code for this sale
        qr_data = f"https://yourstore.com/receipt/{sale.id}"  # adjust URL as needed
        qr_img = qrcode.make(qr_data)
        qr_path = os.path.join(current_app.root_path, "static", f"qr_{sale.id}.png")
        qr_img.save(qr_path)

        # 🔥 Refresh CSV after creation
        export_sales_file()

        return redirect(url_for("sales.receipt", id=sale.id))

    return render_template("sales/create.html", products=products, customers=customers)


# Edit an existing sale
@sales_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_sale(id):
    sale = Sale.query.get_or_404(id)
    products = Product.query.all()
    customers = Customer.query.all()
    if request.method == "POST":
        new_product_id = int(request.form["product_id"])
        new_customer_id = int(request.form["customer_id"])
        new_quantity = int(request.form["quantity"])
        product = Product.query.get_or_404(new_product_id)

        # ✅ Recalculate GST when editing
        GST_RATE = 0.18
        subtotal = round(product.price * new_quantity, 2)
        gst_amount = round(subtotal * GST_RATE, 2)
        grand_total = round(subtotal + gst_amount, 2)

        sale.product_id = new_product_id
        sale.customer_id = new_customer_id
        sale.quantity = new_quantity
        sale.total = grand_total
        sale.gst = gst_amount

        db.session.commit()

        # 🔥 Refresh CSV after update
        export_sales_file()

        flash("Sale updated.", "success")
        return redirect(url_for("sales.list_sales"))

    return render_template("sales/edit.html", sale=sale, products=products, customers=customers)


# Receipt page
@sales_bp.route("/<int:id>/receipt")
def receipt(id):
    sale = Sale.query.get_or_404(id)
    return render_template("sales/receipt.html", sale=sale)


# Delete sale
@sales_bp.route("/<int:id>/delete", methods=["POST"])
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()

    # 🔥 Refresh CSV after delete
    export_sales_file()

    flash("Sale deleted.", "success")
    return redirect(url_for("sales.list_sales"))


@sales_bp.route("/export")
def export_sales():
    path = export_sales_file()   # always overwrites instance/sales.csv
    return send_file(path, as_attachment=False, download_name="sales.csv")
