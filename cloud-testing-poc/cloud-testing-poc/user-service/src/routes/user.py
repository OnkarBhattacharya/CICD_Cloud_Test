from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json(silent=True)
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'username and email are required'}), 400
    try:
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'username or email already exists'}), 409
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'invalid JSON body'}), 400
    try:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'username or email already exists'}), 409
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
