from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from expiry_app.forms import RegistrationForm, LoginForm, InventoryForm, RequestForm
from expiry_app.models import Users, Inventory, Requests, Locations
from expiry_app import app, db, bcrypt
from flask_login import login_user,current_user ,logout_user, login_required
from sqlalchemy import func
from datetime import datetime, timedelta
stuff = [
        {
        'id': 10,
           'name': 'Spaghetti',
           'expiry_date': '07/11/2024',
           'image_file': 'images/spagetti.png',
        },
        {
            'id': 11,
            'name': 'Flour',
            'expiry_date': '07/11/2024',
            'image_file': 'images/flour.png',
        },
        {
            'id': 12,
            'name': 'Soda',
            'expiry_date': '07/11/2024',
            'image_file': '',
        },
        {
            'id': 13,
            'name': 'Spaghetti',
            'expiry_date': '07/11/2024',
            'image_file': 'images/spagetti.png',
        },
    {
        'id':14,
        'name': 'Flour',
        'expiry_date': '07/11/2024',
        'image_file': 'images/flour.png',
    },
    {
        'id': 15,
        'name': 'Soda',
        'expiry_date': '07/11/2024',
        'image_file': 'images/juice.png',
    },
    ]



@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        current_stores = Users.query.filter_by(role='Store').all()
        store_data = []
        #the following code just appends a location to the store for display remove if necessary
        for user in current_stores:
            user_data = {
                'id': user.id,
                'email': user.email,
                'password': user.password,
                'role': user.role,
                'name': user.name,
                'contact_number': user.contact_number,
                'image_file': user.image_file,
                'location': '123 Sample Street',
            }
            store_data.append(user_data)
        #test_data
        shops_data = [
            {
                'id': 1,
                'email': '872364827364782',
                'password':'723468723423',
                'role': 'Store',
                'name': 'Shop 2',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },
            {
                'id': 2,
                'email': '872364827364782',
                'password': '723468723423',
                'role': 'Store',
                'name': 'Shop 3',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },
            {
                'id': 3,
                'email': '872364827364782',
                'password': '723468723423',
                'role': 'Store',
                'name': 'Shop 4',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },
            {
                'id': 4,
                'email': '872364827364782',
                'password': '723468723423',
                'role': 'Store',
                'name': 'Shop 6',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },
            {
                'id': 5,
                'email': '872364827364782',
                'password': '723468723423',
                'role': 'Store',
                'name': 'Shop 7',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },
            {
                'id': 6,
                'email': '872364827364782',
                'password': '723468723423',
                'role': 'Store',
                'name': 'Shop 8',
                'contact_number': '746478365836',
                'image_path': 'profile_pictures/logo.png',
                'location': '123 Sample Street'
            },

        ]

        return render_template("home.html",shop_data=store_data, title='Home', stuff= stuff)
    # enter url for landingpage here
    # else:
    #    return render_template("landing.html", title='Landing')
    





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
     return render_template('input.html',title='Inventory',form=form)


@app.route('/inventory/<int:inventory_id>',methods=['GET','POST'])
def product(inventory_id):
     product = Inventory.query.get_or_404(inventory_id)
     product_requests = product.req
     form = RequestForm()
     if form.validate_on_submit():
          request = Requests(status='Requested',product_id=inventory_id,desc=form.desc.data,user_id=current_user.id,quantity=form.quantity.data)
          db.session.add(request)
          db.session.commit()
          flash(f'The request was  successfully added')
          return render_template('productd.html',title='Home')

     return render_template('productd.html',title=product.name,product=product,product_requests=product_requests,form=form)

@app.route('/delete/<int:inventory_id>',methods=['GET','POST'])
def delete(inventory_id):
     product= Inventory.query.get_or_404(inventory_id)
     if product.user_id != current_user.id:
          abort(404)
     db.session.delete(product)
     db.session.commit()
     flash('Product was successfully deleted','success') 
     return render_template('home.html',title='Home')

@app.route('/donate/<int:inventory_id>',methods=['GET','POST'])
def donate(inventory_id):
     product= Inventory.query.get_or_404(inventory_id)
     if product.user_id != current_user.id:
          abort(404)
     product.status = 'Donation'
     db.session.commit()
     flash('Product was put up for donation','success')
     return render_template('home.html',title='Home')

# @app.route('/req/<int:inventory_id>',methods=['GET','POST'])
# def req(inventory_id):
#      form = RequestForm()
#      product = Inventory.query.get_or_404(inventory_id)
#      if product.user_id == current_user.id:
#           abort(404)
#      if form.validate_on_submit():
#           request = Requests(status='Requested',product_id=inventory_id,desc=form.desc.data,user_id=current_user.id,quantity=form.quantity.data)
#           db.session.add(request)
#           db.session.commit()
#           flash(f'The request was  successfully added')
#      return render_template('home.html',title='Home')

@app.route('/manage_req/<int:request_id>/<int:action>',methods=['GET','POST'])
def manage_req(request_id,action):
     req = Requests.query.get(request_id)
     if action == 1:
          req.status = 'Accepted'
          db.session.commit()
     else:
          req.status = 'Declined'
          db.session.commit()

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


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print('test')
    if request.method == 'POST':
        shop_data = request.get_json()
        session['shop_data'] = shop_data
        return jsonify(success=True)
    else:
        print('test')
        shop_id = session.get('shop_data')['id']
        shop_data = Users.query.filter_by(id=shop_id)
        # location = Locations.query.filter_by(id=shop_id)
        # items_available = Inventory.query.filter_by(user_id=shop_id) query call for later
        active_items_of_shop = stuff
        return render_template('profile.html', shop_data=shop_data, stuff = active_items_of_shop)