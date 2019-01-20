'''
Created on Jan 17, 2019

@author: hong li
'''
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from common.common import OrderForm, CategoryList, config
from database.database import Connection
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import Blueprint, render_template, abort

template_dir = os.path.abspath('../templates')
# home_page = Flask(__name__, template_folder=template_dir,static_folder='../static')
home_page = Blueprint('home_page', __name__, template_folder=template_dir, static_folder='../static')


home_page.secret_key = os.urandom(24)


@home_page.route('/')
# @home_page.route('/<page>')
def index():
    form = OrderForm(request.form)
    print(config.config)
    connection = Connection("mysql")
    db = connection.getConnection(config.config)
    cur = connection.getCursor(db)
    
    cur.execute ("select * from category where parent is null")
    category = cur.fetchall();
    print(category)
    products = []
    
    for cat in category:
        print(cat)
        name = cat[1]
        cur.execute("SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (name,)) 
        data = cur.fetchall()
        products.append(CategoryList(cat[3], data));
    
    cur.close()
    db.close()
    return render_template('home.html', products=products, form=form)






