#!/usr/bin/python3
"""This is the db storage class for AirBnB"""
import json
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    __engine = None
    __session = None
    __clsdict = {
        "State": State,
        "City": City,
        "User": User,
        "Place": Place,
        "Review": Review,
        "Amenity": Amenity}

    def __init__(self):
        """ the initializersz
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            environ['HBNB_MYSQL_USER'],
            environ['HBNB_MYSQL_PWD'],
            environ['HBNB_MYSQL_HOST'],
            environ['HBNB_MYSQL_DB']),
            pool_pre_ping=True)
        if 'HBNB_ENV' in environ.keys():
            if environ['HBNB_ENV'] == 'test':
                Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        my_dict = {}
        if cls is None:
            for key, cls in self.__clsdict.items():
                for obj in self.__session.query(cls):
                    my_dict["{}.{}".format(cls.__name__, obj.id)] = obj
        else:
            for obj in self.__session.query(self.__clsdict.get(cls)):
                my_dict["{}.{}".format(
                    self.__clsdict.get(cls).__name__, obj.id)] = obj
        return my_dict

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.query(obj).delete(synchronize_session=False)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(
            bind=self.__engine,
            expire_on_commit=False))

    def close(self):
        """ calling remove session """
        self.__session.close()
