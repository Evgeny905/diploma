from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import Session
import random
from backend.db_depends import get_db
from models.prediction import Prediction_Base
from schemas import Create_Prediction, Update_Prediction

router = APIRouter(prefix="", tags = [""])
templates = Jinja2Templates(directory='templates')
@router.post('/create')
async def create_prediction(db: Annotated[Session, Depends(get_db)], create_prediction: Create_Prediction):
    db.execute(insert(Prediction_Base).values(title=create_prediction.title,
                                              content=create_prediction.content))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
@router.get('/all_predictions')
async def get_all_predictions(db: Annotated[Session, Depends(get_db)]):
    predictions = db.scalars(select(Prediction_Base)).all()
    return predictions
@router.put('/update_prediction')
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
@router.delete('/delete')
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
@router.get("/")
async def Get_Main_Page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('main_page.html', {'request':request})
@router.get("/predictions")
async def Get_Predictions(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('predictions.html', {'request':request})
@router.get("/viewing")
async def Get_Viewing(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    predictions = db.scalars(select(Prediction_Base)).all()
    return templates.TemplateResponse('viewing.html', {'request':request, 'Predictions': predictions})
@router.get("/prediction")
async def Get_Predictions_Random(request: Request, db: Annotated[Session, Depends(get_db)]) -> HTMLResponse:
    predictions = db.scalars(select(Prediction_Base)).all()
    return templates.TemplateResponse('prediction.html', {'request':request, 'Prediction':predictions[random.randint(0,len(predictions)-1)]})