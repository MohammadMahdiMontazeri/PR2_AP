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
            'price_dollar': round(pr.price_toman/dollar,2),
            'type_product': pr.type_product,
        }
        products.append(prd)

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
            'price_dollar': round(ca.price_toman/dollar,2),
            'count': ca.count,
            'total_dollar': round(ca.total_toman/dollar,2),
            'total_toman': ca.total_toman,
        }
        cart.append(car)
    if db.session.query(func.sum(Cart.total_toman)).scalar() == None:
        summ = {'sum_toman':db.session.query(func.sum(Cart.total_toman)).scalar(),
        'sum_dollar': db.session.query(func.sum(Cart.total_dollar)).scalar()}
    else:
        summ = {'sum_toman': round(db.session.query(func.sum(Cart.total_toman)).scalar(),2),
        'sum_dollar': round(db.session.query(func.sum(Cart.total_dollar)).scalar(),2)}
    

    dataa = {'cart': cart, 'sum': summ}
    return render_template('cart.html', dataa=dataa)



@views.route('/admin', methods=['GET'])
def admin():
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
        type_product = request.form.get('myCheckbox')
        if type_product == None:
            type_product = 0
        new_product = None
        if type_product == 0 and product_name and gdrive_link:
            new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count, gdrive_link=gdrive_link, type_product=type_product)
            db.session.add(new_product)
            db.session.commit()
        if type_product == '1' and product_name and gdrive_link:
            new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count, gdrive_link=gdrive_link, type_product=type_product)
            db.session.add(new_product)
            db.session.commit()
        return redirect(url_for('views.upload'))
    products = Products.query.all()
    data = {'products': products}
    return render_template('add-product.html', data=data)

@views.route("/remove-product", methods=["POST"])
def remove_product():
        data = json.loads(request.data)
        product_name = data["product_name"]
        print(product_name)
        product = Products.query.filter_by(product_name=product_name).first()
        if product:
            try:
                in_cart = Cart.query.filter_by(product_name=product_name).first()
                db.session.delete(in_cart)
                db.commit()
            except:
                pass
            db.session.delete(product)
            db.session.commit()
        return redirect(url_for('views.admin'))
  

@views.route("/add-to-cart", methods=["POST"])
def add_to_cart():
  data = json.loads(request.data)
  product_name = data["productName"]
  product = Products.query.filter_by(product_name=product_name).first()
  product_cart = Cart.query.filter_by(product_name=product_name).first()
  if product:
      if product_cart:
          product_cart.count +=1
          product_cart.total_toman = product_cart.count * product_cart.price_toman
          product_cart.total_dollar = product_cart.count * product_cart.price_dollar
          db.session.commit()
          return jsonify({"success": True})
      else:
        price_toman = product.price_toman
        gdrive_link = product.gdrive_link
        price_dollar = round(price_toman / dollar ,2)
        count = 1
        total_toman = count * price_toman
        total_dollar = count * price_dollar
        new_cart_product = Cart(product_name=product_name,price_toman=price_toman,price_dollar=price_dollar,count=count,total_toman=total_toman,total_dollar=total_dollar,gdrive_link=gdrive_link,)
        db.session.add(new_cart_product)
        db.session.commit()
        return jsonify({"success": True})
  else:
    return jsonify({"success": False})
  

@views.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
  data = json.loads(request.data)
  product_name = data["productName"]
  product_item = Cart.query.filter_by(product_name=product_name).first()
  if product_item:
    db.session.delete(product_item)
    db.session.commit()
    return jsonify({"success": True})
  else:
    return jsonify({"success": False})
  

@views.route("/in-count", methods=["POST"])
def in_count():
  data = json.loads(request.data)
  product_name = data["productName"]
  product_item = Cart.query.filter_by(product_name=product_name).first()
  if product_item:
    print(product_item.count)
    product_item.count += 1
    product_item.total_toman = product_item.price_toman * product_item.count
    product_item.total_dollar = product_item.price_dollar * product_item.count
    db.session.commit()
    return jsonify({"success": True})
  else:
    return jsonify({"success": False})
  

@views.route("/de-count", methods=["POST"])
def de_count():
  data = json.loads(request.data)
  product_name = data["productName"]
  product_item = Cart.query.filter_by(product_name=product_name).first()
  if product_item and product_item.count > 1:
    print(product_item.count)
    product_item.count -= 1
    product_item.total_toman = product_item.price_toman * product_item.count
    product_item.total_dollar = product_item.price_dollar * product_item.count
    db.session.commit()
    return jsonify({"success": True})
  else:
    return jsonify({"success": False})
