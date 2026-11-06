from pydantic import BaseModel,Field
class InvestigationCreate(BaseModel): notes:str=Field(min_length=3,max_length=10000)
