from sqlalchemy import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:My1566@localhost/mydb')

Base = declarative_base()
metadata = Base.metadata


class User(Base):

    __tablename__ = "user"
    idUser = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False)
    firstname = Column(String(45))
    lastname = Column(String(45))
    password = Column(String(100))
    email = Column(String(45))
    location_idlocation = Column(Integer, ForeignKey('location.idLocation'))
    advertisments = relationship("Advertisment", backref="user")

    def __str__(self):
        return f"User: {self.username} first name: {self.firstname}," \
               f" last name: {self.lastname},password: {self.password}," \
               f" location: {self.location_idlocation}"

class Category(Base):
    __tablename__ = "category"
    idCategory = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    advertisments = relationship("Advertisment", backref="category")

    def __str__(self):
        return f"category: {self.name}"

class Location(Base):
    __tablename__ = "location"
    idLocation = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    advertisments = relationship("Advertisment", backref="location")
    users = relationship("User", backref="location")

    def __str__(self):
        return f"Location: {self.name}"

class Advertisment(Base):
    __tablename__ = "Advertisement"
    idAdvertisment = Column(Integer, primary_key=True)
    text = Column(String(45), nullable=False)
    DataOfPublishing = Column(DATETIME)
    status = Column(Enum('open', 'close'), default='open')
    idLocation = Column(Integer, ForeignKey('location.idLocation'))
    idCategory = Column(Integer, ForeignKey('category.idCategory'))
    idUser = Column(Integer, ForeignKey('user.idUser'))

    def __str__(self):
        return f"Advertisment: {self.text} date of publishing: " \
               f"{self.DataOfPublishing}, status: {self.status}, location: {self.idLocation}," \
               f" category: {self.idCategory}, user: {self.idUser} "



