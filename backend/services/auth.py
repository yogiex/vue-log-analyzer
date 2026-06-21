import json
from config import Config
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from functools import wraps
from flask import request, jsonify
import os

API_KEY = os.getenv('API_KEY', 'default-secret-key')

def require_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401
        token = auth_header.split(' ')[1]
        try:
            with open('keys/public.pem', 'rb') as f:
                public_key = serialization.load_pem_public_key(f.read())
            payload = jwt.decode(token, public_key, algorithms=['RS256'])
            # Simpan payload untuk rute (opsional)
            request.user_role = payload.get('role')
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def get_public_key():
    with open('keys/public.pem', 'rb') as f:
        return serialization.load_pem_public_key(f.read())

def get_jwks():
    public_key = get_public_key()
    pub_numbers = public_key.public_numbers()
    # Konstruksi JWK
    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": "my-key-1",   # bisa dinamis
        "n": int_to_base64(pub_numbers.n),
        "e": int_to_base64(pub_numbers.e)
    }
    return {"keys": [jwk]}

def int_to_base64(value):
    """Encode integer to Base64URL tanpa padding"""
    import base64
    value_hex = value.to_bytes((value.bit_length() + 7) // 8, 'big')
    return base64.urlsafe_b64encode(value_hex).rstrip(b'=').decode('ascii')