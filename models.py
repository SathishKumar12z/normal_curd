# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Register(Base):
    __tablename__ = "register"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)

# Create the tables in the database
from database import engine
Base.metadata.create_all(bind=engine)
