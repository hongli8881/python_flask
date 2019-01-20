
from common.imports import Connection,flash,os,app, wraps, request, session,sha256_crypt,redirect,url_for,render_template,Form,StringField,PasswordField,validators,Blueprint
from common.common import config

template_dir = os.path.abspath('../templates')

login_page = Blueprint('login_page', __name__, template_folder=template_dir, static_folder='../static')

login_page.secret_key = os.urandom(24)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        connection = Connection("mysql")
        db = connection.getConnection(config.config)
        cur = connection.getCursor(db)
#         cur.execute("SELECT * FROM users WHERE username=%s", [username])
        # Get user by username
#         cur.execute("SELECT id,name, password FROM users WHERE username=%s", [username])
        sql="SELECT u.id,u.name, u.password,r.role_id FROM users u, user_roles r WHERE u.username=%s and u.id=r.user_id"
        cur.execute(sql, [username])
#         print(username)
#         print(result)
        record = cur.fetchall()
        if cur.rowcount == 1:
            # Get stored value
            for data in record:
#             data = cur.fetchone()
                uid = data[0]
                name = data[1]
                password = data[2]
                role=data[3]
            # Compare password
                if sha256_crypt.verify(password_candidate, password):
                    # passed
                    session['logged_in'] = True
                    session['uid'] = uid
                    session['s_name'] = name
                    x = '1'
                    cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                    if role==1:
                        return redirect(url_for('admin_page.admin'))
                    return redirect(url_for('home_page.index'))
    
                else:
                    flash('Incorrect password', 'danger')
                    return render_template('login.html', form=form)
    
        else:
            flash('Username not found', 'danger')
            # Close connection
            
            return render_template('login.html', form=form)
        cur.close()
        db.close()
    return render_template('login.html', form=form)


@login_page.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        connection = Connection("mysql")
        db = connection.getConnection(config.config)
        cur = connection.getCursor(db)
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('home_page.index'))
        cur.close()
        db.close()
    return redirect(url_for('login'))
def is_logged_in(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('home_page.index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):

    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):

    def wrapped():
        return func(*args, **kwargs)

    return wrapped

class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})

