from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

def print_veggie_burgers(veggieBurgers):
	for veggieBurger in veggieBurgers:
		print veggieBurger.id
		print veggieBurger.price
		print veggieBurger.restaurant.name
		print "\n"

def update_veggie_burger_price(veggieBurgers, new_price):
	for veggieBurger in veggieBurgers:
		if veggieBurger.price != new_price:
			veggieBurger.price = new_price
			session.add(veggieBurger)
			session.commit()

if __name__ == "__main__":
	print_veggie_burgers(veggieBurgers)
	update_veggie_burger_price(veggieBurgers, new_price = "$2.99")
	print_veggie_burgers(veggieBurgers)