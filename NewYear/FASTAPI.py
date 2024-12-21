from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, insert, update, select, delete
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.schema import CreateTable
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
engine = create_engine("sqlite:///Fastapi.db", echo = True)
SessionLocal = sessionmaker(bind=engine)
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
templates = Jinja2Templates(directory='templates/FastAPI_Flask')

class Base(DeclarativeBase):
    pass
class Prediction_Base(Base):
    __tablename__='predictions'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    content = Column(String, unique=True, index=True)
print(CreateTable(Prediction_Base.__table__))
class Create_Prediction(BaseModel):
    title: str
    content: str
class Update_Prediction(BaseModel):
    title: str
    content: str
@app.post('/create')
async def create_prediction(db: Annotated[Session, Depends(get_db)], create_prediction: Create_Prediction):
    db.execute(insert(Prediction_Base).values(title=create_prediction.title,
                                              content=create_prediction.content))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
@app.get('/all_predictions')
async def get_all_predictions(db: Annotated[Session, Depends(get_db)]):
    predictions = db.scalars(select(Prediction_Base)).all()
    return predictions
@app.put('/update_prediction')
async def update_prediction(db: Annotated[Session, Depends(get_db)], prediction_id: int, update_prediction: Update_Prediction):
    prediction = db.scalar(select(Prediction_Base).where(Prediction_Base.id == prediction_id))
    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no prediction found'
        )
    db.execute(update(Prediction_Base).where(Prediction_Base.id == prediction_id).values(
        title=update_prediction.title,
        content=update_prediction.content))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Prediction update is successful'
    }
@app.delete('/delete')
async def delete_prediction(db: Annotated[Session, Depends(get_db)], prediction_id: int):
    prediction = db.scalar(select(Prediction_Base).where(Prediction_Base.id == prediction_id))
    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no prediction found'
        )
    else:
        db.execute(delete(Prediction_Base).where(Prediction_Base.id == prediction_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Prediction delete is successful'
    }
@app.get("/")
async def Get_Main_Page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('main_page.html', {'request':request})
@app.get("/predictions")
async def Get_Predictions(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('predictions.html', {'request':request})
@app.get("/viewing")
async def Get_Viewing(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    predictions = db.scalars(select(Prediction_Base)).all()
    return templates.TemplateResponse('viewing.html', {'request':request, 'Predictions': predictions})
@app.get("/prediction")
async def Get_Predictions_Random(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    predictions = db.scalars(select(Prediction_Base)).all()
    return templates.TemplateResponse('prediction.html', {'request':request, 'Prediction':predictions[random.randint(0,len(predictions)-1)]})