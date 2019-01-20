from common.imports import Connection,flash,os,app, wraps, request, session,sha256_crypt,redirect,url_for,render_template,Form,StringField,PasswordField,validators,Blueprint
from common.common import config

template_dir = os.path.abspath('../templates')

admin_page = Blueprint('admin_page', __name__, template_folder=template_dir, static_folder='../static')

@admin_page.route('/admin')
# @is_admin_logged_in
def admin():
    connection = Connection("mysql")
    db = connection.getConnection(config.config)
    curso = connection.getCursor(db)
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)