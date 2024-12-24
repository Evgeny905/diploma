from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./Predictions_base.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
class Prediction_Base(Base):
    __tablename__='predictions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String, unique=True, index=True)
print(CreateTable(Prediction_Base.__table__))
Base.metadata.create_all(bind=engine)