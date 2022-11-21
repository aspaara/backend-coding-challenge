import json
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./planning.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

with open("planning.json") as file:
    data = json.load(file)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, unique=True, nullable=False
    ),
    sqlalchemy.Column("original_id", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("talent_id", sqlalchemy.String),
    sqlalchemy.Column("talent_name", sqlalchemy.String),
    sqlalchemy.Column("talent_grade", sqlalchemy.String),
    sqlalchemy.Column("booking_grade", sqlalchemy.String),
    sqlalchemy.Column("operating_unit", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("office_city", sqlalchemy.String),
    sqlalchemy.Column("office_postal_code", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("job_manager_name", sqlalchemy.String),
    sqlalchemy.Column("job_manager_id", sqlalchemy.String),
    sqlalchemy.Column("total_hours", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("start_date", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("end_date", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("client_name", sqlalchemy.String),
    sqlalchemy.Column("client_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("industry", sqlalchemy.String),
    sqlalchemy.Column("required_skills", sqlalchemy.JSON),
    sqlalchemy.Column("optional_skills", sqlalchemy.JSON),
    sqlalchemy.Column("is_unassigned", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class User(BaseModel):
    id: int
    original_id: str
    talent_id: str
    talent_name: str
    talent_grade: str
    booking_grade: str
    operating_unit: str
    office_city: str
    office_postal_code: str
    job_manager_name: str
    job_manager_id: str
    total_hours: float
    start_date: str
    end_date: str
    client_name: str
    client_id: str
    industry: str
    required_skills: list[dict]
    optional_skills: list[dict]
    is_unassigned: bool


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/users/", response_model=List[User])
async def read_entries():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=User)
async def create_entry(user: User):
    query = users.insert().values(text=user.text, completed=user.completed)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
