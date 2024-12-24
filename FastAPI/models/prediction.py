from backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import CreateTable

class Prediction_Base(Base):
    __tablename__='predictions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String, unique=True, index=True)
print(CreateTable(Prediction_Base.__table__))