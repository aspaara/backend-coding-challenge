"""Trying out with Flask before using FastAPI"""

import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "planning.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

with open("planning.json") as file:
    data = json.load(file)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    original_id = db.Column(db.String(100), unique=True, nullable=False)
    talent_id = db.Column(db.String(100))
    talent_name = db.Column(db.String(50))
    talent_grade = db.Column(db.String(50))
    booking_grade = db.Column(db.String(50))
    operating_unit = db.Column(db.String(50), nullable=False)
    office_city = db.Column(db.String(50))
    office_postal_code = db.Column(db.String(50), nullable=False)
    job_manager_name = db.Column(db.String(50))
    job_manager_id = db.Column(db.String(100))
    total_hours = db.Column(db.Float(80), nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    client_name = db.Column(db.String(50))
    client_id = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    required_skills = db.Column(db.JSON)
    optional_skills = db.Column(db.JSON)
    is_unassigned = db.Column(db.Boolean(50))

    def __repr__(self):
        return f"<User {self.originalId}>"

    def __init__(
        self,
        original_id,
        talent_id,
        talent_name,
        talent_grade,
        booking_grade,
        operating_unit,
        office_city,
        office_postal_code,
        job_manager_name,
        job_manager_id,
        total_hours,
        start_date,
        end_date,
        client_name,
        client_id,
        industry,
        required_skills,
        optional_skills,
        is_unassigned,
    ):
        self.original_id = original_id
        self.talent_id = talent_id
        self.talent_name = talent_name
        self.talent_grade = talent_grade
        self.booking_grade = booking_grade
        self.operating_unit = operating_unit
        self.office_city = office_city
        self.office_postal_code = office_postal_code
        self.job_manager_name = job_manager_name
        self.job_manager_id = job_manager_id
        self.total_hours = total_hours
        self.start_date = start_date
        self.end_date = end_date
        self.client_name = client_name
        self.client_id = client_id
        self.industry = industry
        self.required_skills = required_skills
        self.optional_skills = optional_skills
        self.is_unassigned = is_unassigned


with app.app_conterecordt():
    for record in data:
        entry = User(
            record["originalId"],
            record["talentId"],
            record["talentName"],
            record["talentGrade"],
            record["bookingGrade"],
            record["operatingUnit"],
            record["officeCity"],
            record["officePostalCode"],
            record["jobManagerName"],
            record["jobManagerId"],
            record["totalHours"],
            record["startDate"],
            record["endDate"],
            record["clientName"],
            record["clientId"],
            record["industry"],
            record["isUnassigned"],
            record["requiredSkills"],
            record["isUnassigned"],
        )
        db.session.add(entry)
        db.session.commit()
