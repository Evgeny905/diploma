from pydantic import BaseModel

class Create_Prediction(BaseModel):
    title: str
    content: str
class Update_Prediction(BaseModel):
    title: str
    content: str