from app import db
from datetime import datetime

class Bus(db.Model):
    __tablename__ = 'buses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    seat_map = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: one bus → many bookings
    bookings = db.relationship('Booking', backref='bus', lazy=True)
