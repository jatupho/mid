from typing import Optional
from pydantic import BaseModel, Field

class WaterSchema(BaseModel):
    message: str

class WaterSchema(BaseModel):
    name: str = Field(...)
    date: int = Field(..., gt=0, lt=32)
    month: int = Field(..., gt=0, lt=13)
    year: int = Field(..., gt=1990, lt=2030)
    water_data_front: float = Field(..., ge=0.0)
    water_data_back: float = Field(..., ge=0.0)
    water_drain_rate: float = Field(..., ge=0.0)


class WaterDataResponse(BaseModel):
    id: int
    name: str
    date: int
    month: int
    year: int
    water_data_front: int
    water_data_back: int
    water_drain_rate: int

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}