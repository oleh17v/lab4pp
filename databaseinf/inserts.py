from datetime import datetime

from tablets import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


session = sessionmaker( bind = engine )
s = session()

location = Location( name = "SomeLocation" )

category = Category( name = "SomeCategory" )


user = User( username = 'RxQu3nn', firstname = 'Roma', lastname = 'Ostrovskiy', password = '1234554321')


advertisment = Advertisment( text = " Some text ",
                             DataOfPublishing = datetime.now(), status = 'open')


s.add(location)
s.add(category)
s.add(advertisment)
s.add(user)
s.commit()