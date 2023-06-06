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
        new_product = Products(product_name=product_name, price_toman=price_toman, price_dollar=price_dollar, count=count,total_toman=total_toman, total_dollar=total_dollar, gdrive_link=gdrive_link)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('views.upload'))
    products = Products.query.all()
    data = {'products': products}
    print(data)
    return render_template('add-product.html', data=data)