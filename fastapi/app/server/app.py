from fastapi import FastAPI
from server.routes.water import router as WaterRouter

app = FastAPI()

app.include_router(WaterRouter, tags=["Water"], prefix="/water")



@app.get("/", tags=["Root"], response_description="Welcome to My REST API server!")
async def read_root():
    return {"message": "My REST API server!"}
