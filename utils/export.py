# utils/export.py
import os
import csv
from flask import current_app
from models import Sale   # import your Sale model

def export_sales():
    # Always overwrite the same file in instance/
    csv_path = os.path.join(current_app.instance_path, "sales.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Sale Code", "Product", "Customer", "Quantity", "Total", "Date"])
        for sale in Sale.query.order_by(Sale.id).all():
            writer.writerow([
                sale.sale_code,
                sale.product.name if sale.product else "",
                sale.customer.name if sale.customer else "",
                sale.quantity,
                sale.total,
                sale.created_at.strftime("%Y-%m-%d %H:%M")
            ])
    return csv_path
