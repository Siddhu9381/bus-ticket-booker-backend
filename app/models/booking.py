from app import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.String, nullable=False)  # Firebase user UID
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    seat_number = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
