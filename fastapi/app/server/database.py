from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData, Column, Integer, String

DATABASE_URL = "postgresql://cpe:Cpe%401234567!@idap.eastus2.cloudapp.azure.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def create_waterdata_table():
    return Table(
        "waterdata",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(255)),
        Column("date", Integer),
        Column("month", Integer),
        Column("year", Integer),
        Column("water_data_front", Integer),
        Column("water_data_back", Integer),
        Column("water_drain_rate", Integer),
    )
def add_water(db: Session, water_data: dict):
    db.execute(waterdata_table.insert().values(water_data))
    db.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()