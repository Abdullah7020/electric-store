from flask import Blueprint, render_template
from models import db, Product, Customer, Supplier, Sale
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates")

@dashboard_bp.route("/dashboard")
def dashboard():
    # Totals
    total_products = Product.query.count()
    total_customers = Customer.query.count()
    total_suppliers = Supplier.query.count()
    total_sales = Sale.query.count()
    revenue = db.session.query(db.func.sum(Sale.total)).scalar() or 0

    # Sales chart data
    sales = Sale.query.order_by(Sale.created_at).all()
    sales_dates = [s.created_at.strftime("%Y-%m-%d") for s in sales]
    sales_totals = [s.total for s in sales]

    return render_template("dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_sales=total_sales,
        revenue=revenue,
        sales_dates=sales_dates,
        sales_totals=sales_totals
    )
