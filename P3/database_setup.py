import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Director(Base):
    __tablename__ = 'director'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    bio = Column(String)
    image = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'         : self.id,
           'bio'         : self.bio,
           'image'         : self.image,
       }
 
class Movie(Base):
    __tablename__ = 'movie'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String)
    trailer = Column(String(250))
    image = Column(String(250))
    director_id = Column(Integer,ForeignKey('director.id'))
    director = relationship(Director) 

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'         : self.description,
           'trailer'         : self.trailer,
           'image'         : self.image,
           'id'         : self.id,
       }


engine = create_engine('sqlite:///directors.db')


Base.metadata.create_all(engine)