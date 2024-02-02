from flask import  render_template, url_for, flash, redirect, request, abort
from expiry_app.forms import RegistrationForm, LoginForm, InventoryForm
from expiry_app.models import Users, Inventory 
from expiry_app import app, db, bcrypt
from flask_login import login_user,current_user ,logout_user, login_required
from sqlalchemy import func
from datetime import datetime, timedelta




@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=['GET', 'POST'])
def home():
     return render_template("home.html",title='Home')
    





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
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password,role=form.role.data,name=form.name.data,location=form.location.data,contact_number=form.contact_number.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} now you can login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
     form = InventoryForm()
     if form.validate_on_submit():
          u_id = current_user.id
          product = Inventory(item_name=form.item_name.data,item_type=form.item_type.data,expiry_date=form.expiry_date.data,quantity=form.quantity.data,user_id=u_id,status='InStock')
          db.session.add(product)
          db.session.commit()
          flash(f'Inventory details were submitted successfully','success')
     return render_template('inventory.html',title='Inventory',form=form)


@app.route('/inventory/<int:inventory_id>')
def product(inventory_id):
     product = Inventory.query.get_or_404(inventory_id)
     return render_template('product.html',title=product.item_name,product=product)

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
     