from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import Cart, Products
from werkzeug.utils import secure_filename
from . import db, create_database
import json
from .api import dollar

views = Blueprint('views', __name__)

@views.route('/add-product', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        product_name = request.form.get('productName')
        price_toman = request.form.get('priceToman')
        price_toman = int(price_toman)
        gdrive_link = request.form.get('gdriveLink')
        price_dollar = price_toman / dollar
        count = 1
        total_toman = count * price_toman
        total_dollar = count * price_dollar
        new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count, gdrive_link=gdrive_link)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('views.upload'))
    products = Products.query.all()
    data = {'products': products}
    return render_template('add-product.html', data=data)

@views.route('/index', methods=['GET'])
def send():
    products_obj = Products.query.all()
    products = []
    for pr in products_obj:
        prd = {
            'product_name': pr.product_name,
            'gdrive_link': pr.gdrive_link,
            'price_toman': pr.price_toman,
            'price_dollar': pr.price_toman/dollar,
        }
        products.append(prd)

    print(products)
    data = {'products': products}
    return render_template('index.html', data=data)

# @views.route('decrese-product', methods=['POST'])
# def decrease_product():
#     product_name = json.loads(request.data('product'))
#     product = Product.objects.get(name=product_name)
#     if product:
#         product.count -= 1

@views.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        product_nammme = request.form.get('pn')
        product = Products.query.filter_by(product_name=product_nammme).first()
        print(product, product_nammme)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('views.admin'))
    products = Products.query.all()
    data = {'products': products}
    return render_template('admin.html', data=data)