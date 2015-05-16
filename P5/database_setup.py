from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    image = Column(String)
    create_date = Column(Date, nullable=False)
    last_update = Column(Date)


class Director(Base):
    __tablename__ = 'director'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    bio = Column(String)
    image = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    create_date = Column(Date, nullable=False)
    last_update = Column(Date)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'name'  : self.name,
                'id'    : self.id,
                'bio'   : self.bio,
                'image' : self.image,
                }


class Movie(Base):
    __tablename__ = 'movie'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String)
    trailer = Column(String)
    image = Column(String)
    director_id = Column(Integer, ForeignKey('director.id'))
    director = relationship(Director)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    create_date = Column(Date, nullable=False)
    last_update = Column(Date)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {'name'         : self.name,
                'description'  : self.description,
                'trailer'      : self.trailer,
                'image'        : self.image,
                'id'           : self.id,
                }


engine = create_engine('postgresql://catalog:udacity@localhost/catalog')


Base.metadata.create_all(engine)
