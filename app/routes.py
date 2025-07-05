from flask import Blueprint, render_template

main = Blueprint('main', __name__)

products = [
    {"id": 1, "name": "T-shirt", "price": 20},
    {"id": 2, "name": "Mug", "price": 10},
    {"id": 3, "name": "Notebook", "price": 15}
]

@main.route('/')
def index():
    return render_template("index.html", products=products)

@main.route('/product/<int:product_id>')
def product(product_id):
    item = next((p for p in products if p["id"] == product_id), None)
    return render_template("product.html", product=item)
