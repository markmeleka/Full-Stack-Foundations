from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	output = ''
	for i in items:
		output += '%s</br>' % i.name
		output += '%s</br>' % i.price
		output += '%s</br>' % i.description
		output += '</br>'
	return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/item/new/')
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	output = ""
	output += "<html><body>"
	output += "<h1>New menu item</h1>" 
	output += "<h2>Restaurant: %s </h2>" % restaurant.name
	output += "<form method = 'POST' enctype = 'multipart/form-data action = /restaurants/<int:restaurant_id>/menu/item/new/'>"
	output += "<input type='text' placeholder='Item Name' required></br>"
	output += "<input type='text' placeholder='Description'></br>"
	output += "<input type='text' placeholder='Price'></br>"
	output += "<input type='text' placeholder='Course'></br>"
	output += "<input type='submit' value='Create'>"
	output += "</form></html></body>"
	return output

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/item/<int:item_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	# menu_item = session.query(MenuItem).filter_by(id=item_id).one()
    
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/item/<int:item_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	# menu_item = session.query(MenuItem).filter_by(id=item_id).one()
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port=5000)