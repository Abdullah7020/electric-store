from flask import Flask, render_template, send_file
from config import Config
from models import db
from routes.products import products_bp
from routes.customers import customers_bp
from routes.suppliers import suppliers_bp
from routes.sales import sales_bp
from routes.dashboard import dashboard_bp
from flask_migrate import Migrate
from utils.export import export_sales
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
    app.register_blueprint(sales_bp, url_prefix="/sales")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    @app.route("/")
    def index():
        return render_template("index.html")

    # 🔹 Export route: regenerates and serves the single CSV
    @app.route("/export/sales")
    def export_sales_route():
        path = export_sales()  # overwrites instance/sales.csv
        return send_file(path, as_attachment=False, download_name="sales.csv")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

    
