
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Order Place'})
class CategoryList(object):

    def __init__(self, category, products):
        self.category = category
        self.products = products
        
class config ():
     config = {
        'host': 'localhost',
        'port': 55555,
        'database': 'mysql',
        'user': 'root',
        'password': '',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }
     
class ProductList(object):

    def __init__(self,id,pName,price,description,available,category,item,pCode,picture):
        self.id=id
        self.pName=pName
        self.price=price
        self.description=description
        self.available=available
        self.category=category
        self.item=item
        self.pCode=pCode
        self.picture=picture