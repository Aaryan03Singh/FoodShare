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
    location = db.Column(db.String(250),nullable=False)
    contact_number = db.Column(db.String(15),unique=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='logo.png')
    product = db.relationship('Inventory',backref='store',lazy=True)

    
    # store = db.relationship('Store',backref='user',lazy=True)

    def __repr__(self):         
        return f"User('{self.username}')"
    
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30),nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('inventory.id'),nullable=False)
    desc = db.Column(db.String(1000),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Request('{self.status}','{self.product_id}')"

    

    
# class Store(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100),unique=True,nullable=False)
#     location = db.Column(db.String(250),nullable=False)
#     contact_number = db.Column(db.String(15),unique=True,nullable=False)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False) 
#     product = db.relationship('Inventory',backref='store',lazy=True)

#     def __repr__(self):
#         return f"Store('{self.name}','{self.user_id}')"
    
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100),nullable=False)
    item_type = db.Column(db.String(100),nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    status = db.Column(db.String(30),nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='logo.png')
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    requests = db.relationship('Requests',backref='requests',lazy=False)

    def __repr__(self):
        return f"Product('{self.item_name}','{self.expiry_date}')"
    