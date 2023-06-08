from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from .models import Cart, Products
from werkzeug.utils import secure_filename
from . import db, create_database
import json
from .api import dollar
from sqlalchemy import func

views = Blueprint('views', __name__)



@views.route('/index', methods=['GET'])
def send():
    products_obj = Products.query.all()
    products = []
    for pr in products_obj:
        prd = {
            'product_name': pr.product_name,
            'gdrive_link': pr.gdrive_link,
            'price_toman': pr.price_toman,
            'price_dollar': round(pr.price_toman/dollar,3),
            'type_product': pr.type_product,
        }
        products.append(prd)

    print(products)
    data = {'products': products}
    return render_template('index.html', data=data)

@views.route('/cart', methods=['GET'])
def send_cart():
    cart_obj = Cart.query.all()
    cart = []
    for ca in cart_obj:
        car = {
            'product_name': ca.product_name,
            'gdrive_link': ca.gdrive_link,
            'price_toman': ca.price_toman,
            'price_dollar': round(ca.price_toman/dollar,3),
            'count': ca.count,
            'total_dollar': round(ca.total_toman/dollar,3),
            'total_toman': ca.total_toman,
        }
        cart.append(car)
    
    summ = {'sum_toman': db.session.query(func.sum(Cart.total_toman)).scalar(),
    'sum_dollar': db.session.query(func.sum(Cart.total_dollar)).scalar()}
    

    dataa = {'cart': cart, 'sum': summ}
    return render_template('cart.html', dataa=dataa)



@views.route('/admin', methods=['GET','POST','DELETE'])
def admin():
    if request.method == 'DELETE':
        product_nammme = request.form.get('pn')
        product = Products.query.filter_by(product_name=product_nammme).first()
        print(product, product_nammme)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('views.admin'))
    products = Products.query.all()
    data = {'products': products}
    return render_template('admin.html', data=data)

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
        type_product = 0
        if request.form.get('myCheckbox') == 1:
            type_product = 1
        if type_product == 0:
            new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count, gdrive_link=gdrive_link, type_product=0)
        elif type_product == 1:
            new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count, gdrive_link=gdrive_link, type_product=1)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('views.upload'))
    products = Products.query.all()
    data = {'products': products}
    return render_template('add-product.html', data=data)


@views.route('/add-to-cart', methods=['POST'])
def addCart():
    product_name = request.form.get('productName')
    product = Product.objects.get(name=product_name)
    new_cart_product = Cart(product_name=Product.product_name, price_toman=Product.price_toman, price_dollar=Product.price_dollar, count=Product.count, gdrive_link=Product.gdrive_link)
    db.session.add(new_cart_product)
    db.session.commit()
    return redirect(url_for('views.index'))


@views.route('decrese-product', methods=['POST'])
def decrease_product():
    product_name = json.loads(request.data('product'))
    product = Product.objects.get(name=product_name)
    
    db.session.delete(product)
    if product and product.count > 1:
        product.count -= 1


@views.route('increase-product', methods=['POST'])
def increase_product():
    product_name = json.loads(request.data('product'))
    product = Product.objects.get(name=product_name)
    if product:
        product.count += 1