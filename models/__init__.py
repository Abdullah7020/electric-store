from datetime import datetime

# Simple in-memory storage (replace with CSV/JSON if you want persistence)
suppliers = []
products = []
customers = []
sales = []
users = []

class Supplier:
    def __init__(self, id, name, contact_email=None, phone=None, address=None):
        self.id = id
        self.name = name
        self.contact_email = contact_email
        self.phone = phone
        self.address = address
        self.products = []

class Product:
    def __init__(self, id, name, sku, price, stock=0, supplier=None):
        self.id = id
        self.name = name
        self.sku = sku
        self.price = price
        self.stock = stock
        self.supplier = supplier

class Customer:
    def __init__(self, id, name, email=None, phone=None, address=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class Sale:
    def __init__(self, id, sale_code, product, customer, quantity, total, gst=0.0):
        self.id = id
        self.sale_code = sale_code
        self.product = product
        self.customer = customer
        self.quantity = quantity
        self.total = total
        self.gst = gst
        self.created_at = datetime.utcnow()

class User:
    def __init__(self, id, username, password, role="admin"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
