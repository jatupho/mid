from server.database import get_db, create_waterdata_table,add_water
from sqlalchemy.orm import Session
from server.models.water import ErrorResponseModel,ResponseModel,WaterSchema, WaterDataResponse
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from fastapi.encoders import jsonable_encoder

router = APIRouter()
waterdata = create_waterdata_table()
# ... (ส่วนที่เหลือเหมือนเดิม)



@router.get("/waterdata/", response_model=List[WaterDataResponse], tags=["Water"])
def read_all_waterdata(
    db: Session = Depends(get_db),
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(100, le=100)
):
    results = db.execute(waterdata.select().offset(skip).limit(limit)).fetchall()
    return [WaterDataResponse(**result._asdict()) for result in results]


# ต่อไปคือฟังก์ชันอื่นๆที่ใช้ waterdata



@router.get("/waterdata/{waterdata_id}", response_model=WaterDataResponse, tags=["Water"])
def read_waterdata(waterdata_id: int = Path(..., title="The ID of the water data to retrieve"), db: Session = Depends(get_db)):
    result = db.execute(waterdata.select().where(waterdata.c.id == waterdata_id)).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="WaterData not found")

    return WaterDataResponse(**result._asdict())



@router.post("/", response_description="Water data added into the database")
async def add_water_data(request_water: WaterSchema = Body(...), db: Session = Depends(get_db)):
    request_water = jsonable_encoder(request_water)
    new_water = add_water(db, request_water)
    return ResponseModel(new_water, "Water added successfully.")