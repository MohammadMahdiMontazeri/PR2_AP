from flask import Blueprint, render_template, request, flash, jsonify
from .models import Cart, Products, Img
from werkzeug.utils import secure_filename
from . import db, create_database
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    pass

@views.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        return f'Uploaded: {file.filename}'
    return render_template('upload.html')

