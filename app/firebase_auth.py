import os
import firebase_admin
from firebase_admin import auth, credentials
from flask import request, jsonify
from functools import wraps

# Load Firebase credentials
cred_path = os.getenv("FIREBASE_CREDENTIAL_PATH")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def firebase_auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Missing Authorization Header"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token  # Attach user to request
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        return f(*args, **kwargs)
    return wrapper
