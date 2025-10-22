from flask import Blueprint, request, jsonify
from ..database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'msg': 'auth ok'})