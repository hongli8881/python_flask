from common.imports import Connection, flash, os, wraps, request, session, sha256_crypt, redirect, url_for, render_template, Form, StringField, PasswordField, validators, Blueprint, UploadSet, configure_uploads
from common.common import config,ProductList
from common.imports import IMAGES
from flask import Flask
from app import vivi_app
import uuid
template_dir = os.path.abspath('../templates')

admin_page = Blueprint('admin_page', __name__, template_folder=template_dir, static_folder='../static')
# admin_page.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'

photos = UploadSet('photos', IMAGES)
vivi_app.config['UPLOADED_PHOTOS_DEST'] = 'static/image/product'
configure_uploads(vivi_app, photos)


@admin_page.route('/admin')
# @is_admin_logged_in
def admin():
    connection = Connection("mysql")
    db = connection.getConnection(config.config)
    curso = connection.getCursor(db)
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    products=[]
    for p in result:
                   print(p)          
                   products.append(ProductList(p[0],p[1], p[2],p[3],p[4],p[5],p[6],p[7],p[8]))
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    curso.close()
    db.close()
    return render_template('pages/index.html', result=products, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)

    
@admin_page.route('/admin_add_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        description = request.form['description']
        available = request.form['available']
        category = request.form['category']
        item = request.form['item']
        code = request.form['code']
        file = request.files['picture']
        print(request.base_url)
        print(vivi_app.config.get('BASE_URL'))
        if name and price and description and available and category and item and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file, folder=category)
#                 save_photo=saveToImage(imageFile=file, filename=pic)
                if save_photo:
                    # Create Cursor
                    connection = Connection("mysql")
                    db = connection.getConnection(config.config)
                    curs = connection.getCursor(db)
                    curs.execute("INSERT INTO products(pName,price,description,available,category,item,pCode,picture)"
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                                 (name, price, description, available, category, item, code, picture))
                    db.commit()
                    product_id = curs.lastrowid
                    curs.execute("INSERT INTO product_level(product_id)" "VALUES(%s)", [product_id])
                    if category == 'tshirt':
                        level = request.form.getlist('tshirt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            db.commit()
                    elif category == 'wallet':
                        level = request.form.getlist('wallet')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            db.commit()
                    elif category == 'belt':
                        level = request.form.getlist('belt')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            db.commit()
                    elif category == 'shoes':
                        level = request.form.getlist('shoes')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            db.commit()
                    elif category == 'cable':
                        level = request.form.getlist('cable')
                        for lev in level:
                            yes = 'yes'
                            query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(field=lev)
                            curs.execute(query, (yes, product_id))
                            # Commit cursor
                            db.commit()                           
                    else:
                        flash('Product level not fund', 'danger')
                        return redirect(url_for('admin_page.edit_product'))
                    # Close Connection
                    curs.close()

                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_page.admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_page.admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_page.admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_page.admin_add_product'))
    else:
        return render_template('pages/add_product.html')


def saveToImage(imageFile=None, filename=None):
#     imageName = str(uuid.uuid4()) + extension
    imageName = filename
    imageDirectory = os.path.join('http://127.0.0.1:8080', 'static', 'upload')
#     imageDirectory = os.path.join(app.config.get('BASE_URL'), 'static', 'upload', 'image')
    imagePath = os.path.join(imageDirectory, imageName)
    image = open(imagePath, "wb")
    image.write(imageFile.decode('base64'))
    image.close()
    
    return imageName


@admin_page.route('/edit_product', methods=['POST', 'GET'])
# @is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        connection = Connection("mysql")
        db = connection.getConnection(config.config)
        curso = db.cursor(buffered=True)
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        curso.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))
        product_level = curso.fetchall()
        if product:
            print(request.method)
            if request.method == 'POST':
                print('post')
                name = request.form.get('name')
                price = request.form['price']
                description = request.form['description']
                available = request.form['available']
                category = request.form['category']
                item = request.form['item']
                code = request.form['code']
                file = request.files['picture']
                # Create Cursor
                if name and price and description and available and category and item and code and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "_")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            cur = db.cursor(buffered=True)
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, available=%s, category=%s, item=%s, pCode=%s, picture=%s WHERE id=%s",
                                (name, price, description, available, category, item, code, pic, product_id))
                            print(exe)
                            if exe:
                                if category == 'tshirt':
                                    level = request.form.getlist('tshirt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        db.commit()
                                elif category == 'wallet':
                                    level = request.form.getlist('wallet')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        db.commit()
                                elif category == 'belt':
                                    level = request.form.getlist('belt')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        db.commit()
                                elif category == 'shoes':
                                    level = request.form.getlist('shoes')
                                    for lev in level:
                                        yes = 'yes'
                                        query = 'UPDATE product_level SET {field}=%s WHERE product_id=%s'.format(
                                            field=lev)
                                        cur.execute(query, (yes, product_id))
                                        # Commit cursor
                                        db.commit()
                                else:
                                    flash('Product level not fund', 'danger')
                                    return redirect(url_for('admin_add_product'))
                                flash('Product updated', 'success')
                                return redirect(url_for('admin_page.edit_product'))
                            else:
                                flash('Data updated', 'success')
                                return redirect(url_for('admin_page.edit_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product,
                                                   product_level=product_level)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product,
                                               product_level=product_level)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product,
                                           product_level=product_level)
            else:
                print('get')
                products = []
                for p in product:
                    print(p)          
                    products.append(ProductList(p[0],p[1], p[2],p[3],p[4],p[5],p[6],p[7],p[8]))
                return render_template('pages/edit_product.html', product=products, product_level=product_level)
        else:
            return redirect(url_for('admin_page.admin'))
    else:
        return redirect(url_for('admin_page.admin'))
