from datetime import date
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# from passhasher import hash_string_bcrypt, check_string_bcrypt, gensalt_bcrypt

# Tworzenie bazy danych
engine = create_engine('sqlite:///tutorial2.db', echo=True)
Base = declarative_base()

# Definicja tego czym użytkownik jest
class User(Base):
  __tablename__ = "users_test"
  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String, index=False)
  password = Column(String)

  def __init__(self, username, password):
    self.username = username
    # self.saltstring = gensalt_bcrypt()
    self.password = password


# # Metoda do tworzenia sesji
def return_sqlalchemysession():
  Session = sessionmaker(bind=engine)
  session = Session()
  return session

Base.metadata.create_all(engine)
