from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import random
app = FastAPI()
templates = Jinja2Templates(directory='NewYear|templates')
predictions = []
class Prediction(BaseModel):
    id: int = None
    title: str
    content: str
@app.get("/")
async def Get_Main_Page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('main_page.html', {'request':request})
@app.get("/predictions")
async def Get_Predictions(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('predictions.html', {'request':request})
@app.get("/viewing")
async def Get_Viewing(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('viewing.html', {'request':request, 'Predictions':predictions})
@app.get("/prediction")
async def Get_Predictions_Random(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('prediction.html', {'request':request, 'Prediction':predictions[random.randint(0,len(predictions)-1)]})



@app.get("/prediction/{prediction_id}")
async def Get_Predictions(request: Request, predictions_id: int) -> HTMLResponse:
    Error = True
    for get_prediction in predictions:
        if get_prediction.id == predictions_id:
            Error = False
            return templates.TemplateResponse('prediction.html', {'request': request, 'Prediction': get_prediction})
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='Prediction was not found')
@app.post("/prediction/{title}/{content}")
async def Create_Predictions(current_Prediction: Prediction, title: Annotated[str, Path(min_length=2, max_length=30, description='Enter title', example='Study at Urban University')],
                       content: Annotated[str, Path(min_length=10, max_length=500, description='Enter content', example='Urban University specializes in teaching IT specialties. It is the best online university in this field.')]) -> Prediction:
    if len(predictions) == 0:
        current_Prediction.id = 1
        current_Prediction.title = title
        current_Prediction.content = content
        predictions.append(current_Prediction)
        return current_Prediction
    else:
        current_Prediction.id = predictions[-1].id + 1
        current_Prediction.title = title
        current_Prediction.content = content
        predictions.append(current_Prediction)
        return current_Prediction
@app.put("/prediction/{prediction_id}/{title}/{content}")
async def Update_Predictions(prediction_id: Annotated[int, Path(ge=1, le=100, description='Enter prediction ID', example='5')],
                       title: Annotated[str, Path(min_length=2, max_length=30, description='Enter title', example='Study at Urban University')],
                       content: Annotated[str, Path(min_length=10, max_length=500, description='Enter content', example='Urban University specializes in teaching IT specialties. It is the best online university in this field.')]) -> Prediction:
    Error = True
    for edit_prediction in predictions:
        if edit_prediction.id == prediction_id:
            Error = False
            edit_prediction.title = title
            edit_prediction.contenr = content
            return edit_prediction
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='Prediction was not found')
@app.delete("/prediction/{prediction_id}")
async def Delete_Predictions(prediction_id: Annotated[int, Path(ge=1, le=100, description='Enter prediction ID', example='5')]) -> Prediction:
    Error = True
    i = -1
    for delete_prediction in predictions:
        i += 1
        if delete_prediction.id == prediction_id:
            Error = False
            predictions.pop(i)
            return delete_prediction
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='Prediction was not found')