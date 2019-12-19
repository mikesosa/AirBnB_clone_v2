#!/usr/bin/python3
"""This is the place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship, backref
from os import getenv


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60),
                     ForeignKey("cities.id"),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey("users.id"),
                     nullable=False)
    name = Column(String(128),
                  nullable=False)
    description = Column(String(1024),
                         nullable=True)
    number_rooms = Column(Integer,
                          default=0,
                          nullable=False)
    number_bathrooms = Column(Integer,
                              default=0,
                              nullable=False)
    max_guest = Column(Integer,
                       default=0,
                       nullable=False)
    price_by_night = Column(Integer,
                            default=0,
                            nullable=False)
    latitude = Column(Float,
                      nullable=True)
    longitude = Column(Float,
                       nullable=True)
    amenity_ids = []

    # if getenv(HBNB_TYPE_STORAGE) = 'db':
    reviews = relationship("Review",
                           backref="place",
                           cascade="all, delete-orphan")

    amenities = relationship("Amenity",
                             secondary="place_amenity",
                             viewonly="False",
                             backref="place")

    place_amenity = Table(
                            "place_amenity", Base.metadata,
                            Column('place_id',
                                   String(60),
                                   ForeignKey('places.id'),
                                   primary_key=True,
                                   nullable=False),
                            Column('amenity_id',
                                   String(60),
                                   ForeignKey('amenities.id'),
                                   primary_key=True,
                                   nullable=False))

    @property
    def reviews(self):
        """ getter attribute for reviews of places """
        obj = storage.all()
        reviews = []
        print("OBJ:", obj)
        print("MY DICT:", my_dict)
        for key, value in my_dict.items():
            if "Review" in key and value.place_id == self.id:
                reviews.append(value)
        return reviews

    @property
    def amenities(self):
        """ getter attribute for amenities of places """
        obj = storage.all()
        amenities = []
        for k, v in obj:
            if "Amenity" in k and v.place_id == self.id:
                amenities.append(v)
        return amenities
