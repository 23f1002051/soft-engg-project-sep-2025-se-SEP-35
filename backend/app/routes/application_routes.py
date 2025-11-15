from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Application

application_bp = Blueprint('application_bp', __name__)

@application_bp.route('/applications', methods=['GET'])
def get_applications():
    applications = Application.query.all()
    return jsonify([{
        'id': app.id,
        'user_id': app.user_id,
        'job_id': app.job_id,
        'status': app.status,
        'applied_at': app.applied_at
    } for app in applications])

@application_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    app = Application.query.get_or_404(application_id)
    return jsonify({
        'id': app.id,
        'user_id': app.user_id,
        'job_id': app.job_id,
        'status': app.status,
        'applied_at': app.applied_at
    })

@application_bp.route('/applications', methods=['POST'])
def create_application():
    data = request.json
    app = Application(
        user_id=data.get('user_id'),
        job_id=data.get('job_id'),
        status=data.get('status', 'applied')
    )
    db.session.add(app)
    db.session.commit()
    return jsonify({'message': 'Application created', 'id': app.id}), 201

@application_bp.route('/applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    app = Application.query.get_or_404(application_id)
    data = request.json
    app.status = data.get('status', app.status)
    db.session.commit()
    return jsonify({'message': 'Application updated'})

@application_bp.route('/applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    app = Application.query.get_or_404(application_id)
    db.session.delete(app)
    db.session.commit()
    return jsonify({'message': 'Application deleted'})
