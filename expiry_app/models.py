from expiry_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100),unique=True,nullable=False)
    contact_number = db.Column(db.String(15),unique=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='logo.png')
    product = db.relationship('Inventory',backref='products',lazy=True)
    locations = db.relationship('Location',backref='location',lazy=True)
    requests = db.relationship('Requests',backref='request',lazy=True)


    def __repr__(self):         
        return f"User('{self.username}')"
    
class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100),unique=True,nullable=False)
    address = db.Column(db.String(2000),unique=True,nullable=False)
    city = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=False)
    country = db.Column(db.String(100),nullable=False)
    zipcode = db.Column(db.Integer,nullable=False)
    user_id = user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30),nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('inventory.id'),nullable=False)
    desc = db.Column(db.String(1000),nullable=False)
    date = db.Column(db.Date,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Request('{self.status}','{self.product_id}')"

    
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100),nullable=False)
    item_type = db.Column(db.String(100),nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    brand = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(2000))
    quantity = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(30),nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='logo.png')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    requests = db.relationship('Requests',backref='requests',lazy=False)

    def __repr__(self):
        return f"Product('{self.item_name}','{self.expiry_date}')"
    
