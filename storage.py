from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///notify_bot.db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    key = Column(String)
    chat_id = Column(String)
    def __repr__(self):
       return "<User(key='%s', chat_id='%s')>" % (
                            self.key, self.chat_id)

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

def add_key(key, chat_id):
    user = session.query(User).filter_by(chat_id=chat_id).first()
    if user:
        user.key = key
    else:
        user = User(key=key, chat_id=chat_id)
        session.add(user)
    session.commit()
    return True

def get_key(chat_id):
    user = session.query(User).filter_by(chat_id=chat_id).first()
    return user.key

def get_chat_id(key):
    user = session.query(User).filter_by(key=key).first()
    return user.chat_id

