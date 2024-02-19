from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from expiry_app.forms import RegistrationForm, LoginForm, InventoryForm, CheckoutForm
from expiry_app.models import Users, Inventory 
from expiry_app import app, db, bcrypt
from flask_login import login_user,current_user ,logout_user, login_required
from sqlalchemy import func
from datetime import datetime, timedelta

stuff = [
        {
           'name': 'Spaghetti',
           'exp_date': '07/11/2024',
           'image_path': 'images/sample_shop_images/img_8.png',
        },
        {
            'name': 'Flour',
            'exp_date': '07/11/2024',
            'image_path': 'images/sample_shop_images/img_7.png',
        },
        {
            'name': 'Soda',
            'exp_date': '07/11/2024',
            'image_path': 'images/sample_shop_images/img_9.png',
        },
        {
            'name': 'Spaghetti',
            'exp_date': '07/11/2024',
            'image_path': 'images/sample_shop_images/img_8.png',
        },
    {
        'name': 'Flour',
        'exp_date': '07/11/2024',
        'image_path': 'images/sample_shop_images/img_7.png',
    },
    {
        'name': 'Soda',
        'exp_date': '07/11/2024',
        'image_path': 'images/sample_shop_images/img_9.png',
    },
    ]


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=['GET', 'POST'])
def home():
    #  sample data replace with backend call
    shop_data = [
        {
            'name': 'Shop 1',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_0.png',
        },
        {
            'name': 'Shop 2',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_1.png',
        },
        {
            'name': 'Shop 3',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_2.png',
        },
        {
            'name': 'Shop 4',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_3.png',
        },
        {
            'name': 'Shop 5',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_4.png',
        },
        {
            'name': 'Shop 6',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_5.png',
        },
        {
            'name': 'Shop 7',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_6.png',
        },
        {
            'name': 'Shop 8',
            'address': '123 Samplestreet',
            'image_path': 'images/sample_shop_images/img_0.png',
        },
    ]

    return render_template("home.html",title='Home',  shop_data=shop_data, stuff= stuff)
    





@app.route("/all_products", methods=['GET', 'POST'])
@login_required
def all_products():
    expiry_threshold =datetime.utcnow() + timedelta(days=10)
    items_available = Inventory.query.filter_by(user_id=current_user.id)
    return render_template('all_products.html', title='All Products',inventory=items_available,expiry_threshold=expiry_threshold)
    
@app.route("/expiry_products", methods=['GET', 'POST'])
@login_required
def expiry_products():
     expiry_threshold =datetime.utcnow() + timedelta(days=10)
     items_available = Inventory.query.filter(Inventory.expiry_date <= expiry_threshold).filter_by(user_id=current_user.id)
     return render_template('expiry_products.html',title='Expiry Products',inventory=items_available)


 
    
@app.route("/avaliable_products", methods=['GET', 'POST'])
@login_required
def avaliable_products():
     expiry_threshold =datetime.utcnow() + timedelta(days=10)
     items_available = Inventory.query.filter(Inventory.expiry_date <= expiry_threshold)
     return render_template('avaliable_products.html',title='Avaliable Products',inventory=items_available)









@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users( email=form.email.data, password=hashed_password,role=form.role.data,name=form.name.data,contact_number=form.contact_number.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data} now you can login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
     form = InventoryForm()
     if form.validate_on_submit():
          u_id = current_user.id
          product = Inventory(name=form.name.data,category=form.category.data,expiry_date=form.expiry_date.data,quantity=form.quantity.data,user_id=u_id,status='InStock',desc=form.desc.data,brand=form.brand.data)
          db.session.add(product)
          db.session.commit()
          flash(f'Inventory details were submitted successfully','success')
     return render_template('inventory.html',title='Inventory',form=form)


@app.route('/inventory/<int:inventory_id>')
def product(inventory_id):
     product = Inventory.query.get_or_404(inventory_id)
     return render_template('product.html',title=product.name,product=product)

@app.route('/delete/<int:inventory_id>',methods=['GET','POST'])
def delete(inventory_id):
     product= Inventory.query.get_or_404(inventory_id)
     if product.user_id != current_user.id:
          abort(404)
     db.session.delete(product)
     db.session.commit()
     flash('Product was successfully deleted','success') 
     return render_template('home.html',title='Home')

     

     


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                 login_user(user, remember=form.remember.data)
                 next_page = request.args.get('next')
                 return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                 flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('home'))

@app.route("/profile", methods=['GET'])
def profile():
    if request.method == 'GET':
        shop_data = request.args.to_dict()
        return jsonify(shop_data)
    else:
        # Handle other HTTP methods if needed
        return jsonify({'error': 'Method not allowed'}), 405


@app.route("/checkout")
def checkout():
    shop_data = {
        'name': 'Shop 1',
        'address': '123 Samplestreet 400001 Samplecity',
        'image_path': 'images/sample_shop_images/img_0.png',
        'reward_level': 4,
        'points': 233,
    }
    order_data = [
            {
                'name': 'Oranges',
                'amount': 10,
                'cost': 5
            },
        {
            'name': 'Spaghetti',
            'amount': 10,
            'cost': 15
        },
        {
            'name': 'Flour',
            'amount': 3,
            'cost': 20
        },
        ]
    form = CheckoutForm()
    if form.validate_on_submit():
        print('success')
    if current_user.is_authenticated:
        return render_template('checkout.html', user= current_user, shop_data=shop_data, order_data=order_data,
                               cost=calculate_final_amount(order_data), stuff=stuff)
    else:
        return redirect(url_for('home'))


def calculate_final_amount(order_data):

    total_cost = {
        'cost': 0,
        'tax': 0,
        'shipping': 4.99,
        'final_amount': 0
    }
    for entry in order_data:
        total_cost['cost'] += entry['cost']
    total_cost['tax'] = total_cost['cost'] * 0.19
    total_cost['final_amount'] = "%0.2f" % (total_cost['cost'] + total_cost['tax'] + total_cost['shipping'])
    return total_cost
