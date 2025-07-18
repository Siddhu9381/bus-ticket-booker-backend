from flask import Blueprint, request, jsonify
from app import db
from app.models import Bus
from datetime import datetime

bus_bp = Blueprint('bus', __name__)

# 🚌 Search buses by origin, destination, date
@bus_bp.route('/buses/search', methods=['GET'])
def search_buses():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date_str = request.args.get('date')

    if not origin or not destination or not date_str:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format (YYYY-MM-DD expected)'}), 400
    
    print(date_obj)

    buses = Bus.query.filter_by(
        origin=origin,
        destination=destination,
        date=date_obj
    ).all()

    print(buses)

    bus_list = [
        {
            'id': bus.id,
            'name': bus.name,
            'origin': bus.origin,
            'destination': bus.destination,
            'date': bus.date.isoformat()
        } for bus in buses
    ]

    return jsonify(bus_list), 200

# 🚌 Get detailed bus info (including seat map)
@bus_bp.route('/buses/<int:bus_id>', methods=['GET'])
def get_bus(bus_id):
    bus = Bus.query.get(bus_id)
    if not bus:
        return jsonify({'error': 'Bus not found'}), 404

    bus_info = {
        'id': bus.id,
        'name': bus.name,
        'origin': bus.origin,
        'destination': bus.destination,
        'date': bus.date.isoformat(),
        'seat_map': bus.seat_map
    }

    return jsonify(bus_info), 200

# 🛠️ Add new bus (for admin use)
@bus_bp.route('/buses', methods=['POST'])
def add_bus():
    data = request.get_json()
    name = data.get('name')
    origin = data.get('origin')
    destination = data.get('destination')
    date_str = data.get('date')
    seat_map = data.get('seat_map')

    if not all([name, origin, destination, date_str, seat_map]):
        return jsonify({'error': 'Missing data'}), 400

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format (YYYY-MM-DD expected)'}), 400

    new_bus = Bus(
        name=name,
        origin=origin,
        destination=destination,
        date=date_obj,
        seat_map=seat_map
    )
    db.session.add(new_bus)
    db.session.commit()

    return jsonify({'message': 'Bus added successfully', 'id': new_bus.id}), 201
