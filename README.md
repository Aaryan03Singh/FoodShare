# FoodShare

After cloning the repository go to cmd line and open python in the same directory then run the following commands in python

from expiry_app import app,db<br>
app.app_context().push()<br>
db.create_all()<br>
exit()<br>

this will create a local database for testing later we will shift to a postgresql for deployment

To run the program type python run.py in the cmd line

the routes.py contain all the routes for the app
each route has a corresponding html page with is in the templates folder, css and javascript to those templates should to added to the static folder.
Any pictures or logos should be added to the static folder.

In each template in that route certain values are passed thorugh which can be used in the html page
for example in home

return render_template('home.html',product=product)

in the home.html we can use the product variable by enclosing it in {{ }}
to print the product name we can do <.h1> {{product.name }} <./h1>

for any href links in the frontend instead of the link its better to use "{{url_for('foldername',filename='image/filename')}}"

Future functionalities to add-
Add custom images that are inputed from the user
Add request and accpet functionalites for the products
Implement the UI to the flask project
Add update store/organization info page



from expiry_app import app,db
with app.app_context().push()
db.create_all()
db.drop_all()