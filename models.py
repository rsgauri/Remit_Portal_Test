from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = "clients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    contact = db.Column(db.String(50))
    active = db.Column(db.String(10), default="Yes")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Source(db.Model):
    __tablename__ = "sources"
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    type = db.Column(db.String(50))
    active = db.Column(db.String(10), default="Yes")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class RemittanceAdvice(db.Model):
    __tablename__ = "remittance_advice"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer)
    invoice_no = db.Column(db.String(100))
    invoice_date = db.Column(db.String(100))
    invoice_amount = db.Column(db.String(100))
    file_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)