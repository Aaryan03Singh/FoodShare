import os

from flask import render_template, url_for, flash, redirect, request, abort, session, jsonify
from werkzeug.utils import secure_filename

from expiry_app.forms import RegistrationForm, LoginForm, InventoryForm, RequestForm
from expiry_app.models import Users, Inventory, Requests, Locations
from expiry_app import app, db, bcrypt
from flask_login import login_user,current_user ,logout_user, login_required
from sqlalchemy import func
from datetime import datetime, timedelta


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
        expiry_threshold = datetime.utcnow() + timedelta(days=10)
        soon_to_expire_products = Inventory.query \
            .filter(Inventory.status == 'Donation') \
            .order_by(Inventory.expiry_date.asc()) \
            .limit(8)
        for item in soon_to_expire_products:
            item.image_file= os.path.basename(item.image_file)
        for x in current_stores:
            x.image_file= os.path.basename(x.image_file)
        return render_template("home.html",shop_data=store_data, title='Home', stuff=soon_to_expire_products)
    else:
        return redirect(url_for('landingpage'))
    # enter url for landingpage here
    # else:
    #    return render_template("landing.html", title='Landing')
    
@app.route("/landingpage", methods=["GET", "POST"])
def landingpage():
    return render_template("landing_page.html")

@app.route("/about_us", methods=["GET", "POST"])
def about_us():
    return render_template("about_us.html")

@app.route("/contact_us", methods=["GET", "POST"])
def contact_us():
    return render_template("contact_us.html")

@app.route("/layout", methods=["GET", "POST"])
def layout():
    return render_template("layout.html")

@app.route("/orglayout", methods=["GET", "POST"])
def orglayout():
    return render_template("org-layout.html")


@app.route("/all_products", methods=['GET', 'POST'])
@login_required
def all_products():
    expiry_threshold =datetime.utcnow() + timedelta(days=90)
    items_available = Inventory.query.filter_by(user_id=current_user.id)
    for item in items_available:
        item.image_file = os.path.basename(item.image_file)
    return render_template('all_products.html', title='All Products',inventory=items_available,expiry_threshold=expiry_threshold)


@app.route("/all_requests",methods=["GET", "POST"])
@login_required
def all_requests():
    requests = Requests.query.filter_by(user_id=current_user.id)
    requests_with_users = []
    for request in requests:
        requester = Users.query.get(request.user_id)
        product = Inventory.query.get(request.product_id)
        product_owner = Users.query.get(product.user_id)
        requests_with_users.append({
            'request': request,
            'requester_name': requester.name,
            'product_owner_name': product_owner.name,
            'product_name': product.name,
            'product_img': product.image_file
        })
    for x in requests_with_users:
        x['product_img'] = os.path.basename(x['product_img'])
    return render_template('request.html', title='All Requests', requests_with_users=requests_with_users)

@app.route("/expiry_products", methods=['GET', 'POST'])
@login_required
def expiry_products():
     expiry_threshold =datetime.utcnow() + timedelta(days=10)
     items_available = Inventory.query.filter(Inventory.expiry_date <= expiry_threshold).filter_by(user_id=current_user.id)
     for item in items_available:
         item.image_file = os.path.basename(item.image_file)
     return render_template('expiry_products.html',title='Expiry Products',inventory=items_available)


 
    
@app.route("/store_products/<int:store_id>", methods=['GET', 'POST'])
@login_required
def store_products(store_id):
     store= Users.query.get_or_404(store_id)
     expiry_threshold =datetime.utcnow() + timedelta(days=10)
     items_available = Inventory.query.filter(
    Inventory.status == "Donation").filter_by(user_id=store_id).all()
     for item in items_available:
         item.image_file = os.path.basename(item.image_file)
     return render_template('store_products.html',title='Avaliable Products',inventory=items_available,store=store)


@app.route("/available_products", methods=['GET', 'POST'])
@login_required
def available_products():
    products = Inventory.query.filter(Inventory.status == 'Donation').all()
    for item in products:
         item.image_file = os.path.basename(item.image_file)
    return render_template('available_products.html',products=products)







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
     print('test')
     if form.validate_on_submit():
          u_id = current_user.id
          file = form.file_image.data
          filename = secure_filename(file.filename)
          #file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          file_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
          file.save(file_path)
          product = Inventory(name=form.name.data,category=form.category.data,expiry_date=form.expiry_date.data,quantity=form.quantity.data,user_id=u_id,status='InStock',desc=form.desc.data,brand=form.brand.data, image_file=file_path)
          db.session.add(product)
          db.session.commit()
          flash(f'Inventory details were submitted successfully','success')
          return redirect(url_for('all_products'))

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
      return redirect(url_for('product',inventory_id=inventory_id))
    product.image_file=os.path.basename(product.image_file)
    return render_template('productd.html',title=product.name,product=product,product_requests=product_requests,form=form)

    return redirect(url_for('available_products'))

@app.route('/delete/<int:inventory_id>',methods=['GET','POST'])
def delete(inventory_id):
     product= Inventory.query.get_or_404(inventory_id)
     if product.user_id != current_user.id:
          abort(404)
     db.session.delete(product)
     db.session.commit()
     flash('Product was successfully deleted','success') 
     return redirect(url_for('all_products'))

@app.route('/donate/<int:inventory_id>',methods=['GET','POST'])
def donate(inventory_id):
     product= Inventory.query.get_or_404(inventory_id)
     if product.user_id != current_user.id:
          abort(404)
     product.status = 'Donation'
     db.session.commit()
     flash('Product was put up for donation','success')
     return redirect(url_for('all_products',inventory_id=inventory_id))


@app.route('/manage_req/<int:request_id>/<int:action>',methods=['GET','POST'])
def manage_req(request_id,action):
     req = Requests.query.get(request_id)
     if action == 1:
          req.status = 'Accepted'
          db.session.commit()
     elif action == 0:
          db.session.delete(req)
          db.session.commit()
     else:
         req.status = 'Confirmed'
         db.session.commit()
         return redirect(url_for('all_requests'))

     return redirect(url_for('product',inventory_id=req.product_id))
          
     

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
                 if next_page:
                    return redirect(next_page)
                 else:
                    if user.role == 'Store':
                        return redirect(url_for('layout'))
                    elif user.role == 'Organization':
                         return redirect(url_for('orglayout'))
                    else:
                         return redirect(url_for('home'))
            else:
                 flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
     


#@app.route("/login", methods=['GET', 'POST'])
#def login():
   # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
    #form = LoginForm()
    #       user = Users.query.filter_by(email=form.email.data).first()
     #       if user and bcrypt.check_password_hash(user.password, form.password.data):
      #           login_user(user, remember=form.remember.data)
       #          next_page = request.args.get('next')
        #         return redirect(next_page) if next_page else redirect(url_for('home'))
         #   else:
          #       flash('Login Unsuccessful. Please check email and password', 'danger')
    #return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
     logout_user()
     return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        shop_data = request.get_json()
        session['shop_data'] = shop_data
        return jsonify(success=True)
    else:
        shop_id = session.get('shop_data')['id']
        shop_data = Users.query.get_or_404(shop_id)
        items_available = Inventory.query.filter_by(user_id=shop_id)
        for item in items_available:
            item.image_file = os.path.basename(item.image_file)
        return render_template('profile.html', shop_data=shop_data, stuff = items_available)