from home.home import home_page
from flask import Flask
from login.login import login_page
from admin.admin import admin_page
from common.imports import os
vivi_app = Flask(__name__)

# def main(config):
   
vivi_app.register_blueprint(home_page)
vivi_app.register_blueprint(login_page)
vivi_app.register_blueprint(admin_page)
vivi_app.secret_key = os.urandom(24)
vivi_app.run(host='127.0.0.1', port=8080)
