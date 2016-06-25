from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Boolean,
    Date,
    Time,
    ForeignKey,
    func,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )


from sqlalchemy import create_engine

engine = create_engine("sqlite:///ndb.db")
Session = sessionmaker()
Base = declarative_base(bind = engine)

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	login = Column(String, nullable = False)
	password = Column(String, nullable = False)
	name = Column(String, nullable = False)
	lastname = Column(String, nullable = False)
	city = Column(String)
	age = Column(Integer)
	avatar = Column(String, nullable = False)

class Photo(Base):
	__tablename__ = 'photos'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey(User.__tablename__ +'.id'), nullable = False)
	user = relationship("User", backref="photos")
	path = Column(String, nullable = False)

class Friendship(Base):
	__tablename__ = 'friendships'

	id = Column(Integer, primary_key=True)
	user_from_id = Column(Integer, ForeignKey(User.__tablename__ +'.id'), nullable = False)
	user_to_id = Column(Integer,ForeignKey(User.__tablename__ +'.id'), nullable = False)
	dialogLocPath = Column(String, nullable = False)

class Friendrequest(Base):
	__tablename__ = 'friendrequests'

	id = Column(Integer, primary_key=True)
	user_from_id = Column(Integer,ForeignKey(User.__tablename__ +'.id'), nullable = False)
	user_to_id = Column(Integer,ForeignKey(User.__tablename__ +'.id'), nullable = False)		

