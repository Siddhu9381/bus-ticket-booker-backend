from app import create_app, db
from app.models import Bus
from datetime import date

app = create_app()

with app.app_context():
    # Clear existing buses (optional)
    Bus.query.delete()
    
    # Example seat map: 0 = available, 1 = booked, -1 = aisle
    seat_map = [
        [1, 0, -1, 0, 1],
        [1, 1, -1, 0, 0],
        [0, 0, -1, 1, 1],
    ]

    # Create sample buses
    bus1 = Bus(
        name="Express 101",
        origin="City A",
        destination="City B",
        date=date(2025, 7, 20),
        seat_map=seat_map
    )

    bus2 = Bus(
        name="SuperFast 202",
        origin="City C",
        destination="City D",
        date=date(2025, 7, 21),
        seat_map=seat_map
    )

    db.session.add(bus1)
    db.session.add(bus2)
    db.session.commit()

    print("✅ Dummy buses added!")
