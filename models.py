from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# import os
from app import login


# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'mysecret'


db = SQLAlchemy(app)
Migrate(app, db)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __init__(self, name, phone, content):
        self.name = name
        self.phone = phone
        self.content = content

    def __repr__(self):
        return f"('name: {self.name}\ndate: {self.date_posted}\n"


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    total_beds = db.Column(db.Integer, nullable=False)
    available_beds = db.Column(db.Integer, nullable=False)
    total_ward_beds = db.Column(db.Integer, nullable=False)
    available_ward_beds = db.Column(db.Integer, nullable=False)
    total_ward_beds_with_oxygen = db.Column(db.Integer, nullable=False)
    available_ward_beds_with_oxygen = db.Column(db.Integer, nullable=False)
    total_icu_beds = db.Column(db.Integer, nullable=False)
    available_icu_beds = db.Column(db.Integer, nullable=False)
    total_icu_beds_with_oxygen = db.Column(db.Integer, nullable=False)
    available_icu_beds_with_oxygen = db.Column(db.Integer, nullable=False)
    beds = db.relationship('Bed', backref='hospital', lazy=True)

    def __init__(self, name, area, district, state, total_beds, available_beds,
                 total_ward_beds, available_ward_beds, total_ward_beds_with_oxygen,
                 available_ward_beds_with_oxygen, total_icu_beds, available_icu_beds,
                 total_icu_beds_with_oxygen, available_icu_beds_with_oxygen):
        self.name = name
        self.area = area
        self.district = district
        self.state = state
        self.total_beds = total_beds
        self.available_beds = available_beds
        self.total_ward_beds = total_ward_beds
        self.available_ward_beds = available_ward_beds
        self.total_ward_beds_with_oxygen = total_ward_beds_with_oxygen
        self.available_ward_beds_with_oxygen = available_ward_beds_with_oxygen
        self.total_icu_beds = total_icu_beds
        self.available_icu_beds = available_icu_beds
        self.total_icu_beds_with_oxygen = total_icu_beds_with_oxygen
        self.available_icu_beds_with_oxygen = available_icu_beds_with_oxygen

    def __repr__(self):
        return f"name: {self.name}\navailable beds: {self.available_beds}\n"


class Bed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bed_number = db.Column(db.Integer, nullable=False)
    bed_type = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey(
        'hospital.id'), nullable=False)
    patients = db.relationship('Patient', backref='bed', lazy=True)

    def __init__(self, bed_number, bed_type, cost, hospital):
        self.bed_number = bed_number
        self.bed_type = bed_type
        self.cost = cost
        self.hospital = hospital

    def __repr__(self):
        return f"bed number: {self.bed_number}\ntype: {self.bed_type}"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    admit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    blood_group = db.Column(db.String(20), nullable=False)
    bed_id = db.Column(db.Integer, db.ForeignKey('bed.id'), nullable=False)

    def __init__(self, name, age, gender, status, phone, address, blood_group, bed):
        self.name = name
        self.age = age
        self.gender = gender
        self.status = status
        self.phone = phone
        self.address = address
        self.blood_group = blood_group
        self.bed = bed

    def __repr__(self):
        return f"name: {self.name}\nadmit_date: {self.admit_date}"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    role = db.Column(db.String(20))
    phone = db.Column(db.String(10), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    address = db.Column(db.String(120))

    def __init__(self, name,  age, gender, role, phone, email, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.role = role
        self.phone = phone
        self.email = email
        self.address = address

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"name: {self.name}, id: {self.id}, role: {self.role}\n"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
