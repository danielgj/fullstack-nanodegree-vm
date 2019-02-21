#!/usr/bin/env python3
 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

DBSession = sessionmaker(bind = engine)

session = DBSession()

# myFirstRestaurant = Restaurant(name="Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()

pepe = session.query(MenuItem).all()
for item in pepe:
    print "{0}".format(item.name)