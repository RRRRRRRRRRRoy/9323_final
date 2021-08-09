from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from utilities.CONFIG import Database

BaseModel = declarative_base()

mydburi = f'mysql+pymysql://{Database.USER}:{Database.PASSWORD}@localhost:3306/{Database.NAME}?autocommit=true'
engine = create_engine(mydburi, encoding='utf-8')


def NewSession():
  DB_session = sessionmaker(bind=engine)
  return DB_session()


def db_create():
  BaseModel.metadata.create_all(engine)


class User(BaseModel):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), unique=True)
  password = Column(String(255))
  email = Column(String(100), unique=True)
  gender = Column(String(50))
  dob = Column(String(50))
  address = Column(String(200))


class Group(BaseModel):
  __tablename__ = 'group'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), unique=True)
  createtime = Column(String(255))
  description = Column(String(255))
  originator = Column(String(50))


class Roles(BaseModel):
  __tablename__ = 'roles'
  id = Column(Integer, primary_key=True)
  user_id = Column(String(50))
  group_id = Column(String(50))
  role = Column(String(255))


class Meeting(BaseModel):
  __tablename__ = 'meeting'
  id = Column(Integer, primary_key=True)
  name = Column(String(50))
  starttime = Column(String(255))
  endtime = Column(String(255))
  group_id = Column(String(50))

