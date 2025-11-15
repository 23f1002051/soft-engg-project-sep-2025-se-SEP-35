from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Employee, Performance

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': e.id,
        'user_id': e.user_id,
        'job_title': e.job_title,
        'department': e.department,
        'hired_at': e.hired_at,
        'photo': e.photo
    } for e in employees])

@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    e = Employee.query.get_or_404(employee_id)
    return jsonify({
        'id': e.id,
        'user_id': e.user_id,
        'job_title': e.job_title,
        'department': e.department,
        'hired_at': e.hired_at,
        'photo': e.photo,
        'performances': [
            {
                'id': p.id,
                'metric': p.metric,
                'value': p.value,
                'date': p.date
            } for p in e.performances
        ]
    })

@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    e = Employee(
        user_id=data.get('user_id'),
        job_title=data.get('job_title'),
        department=data.get('department'),
        photo=data.get('photo')
    )
    db.session.add(e)
    db.session.commit()
    return jsonify({'message': 'Employee created', 'id': e.id}), 201

@employee_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    e = Employee.query.get_or_404(employee_id)
    data = request.json
    e.job_title = data.get('job_title', e.job_title)
    e.department = data.get('department', e.department)
    e.photo = data.get('photo', e.photo)
    db.session.commit()
    return jsonify({'message': 'Employee updated'})

@employee_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    e = Employee.query.get_or_404(employee_id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({'message': 'Employee deleted'})

# Performance endpoints
@employee_bp.route('/employees/<int:employee_id>/performances', methods=['POST'])
def add_performance(employee_id):
    e = Employee.query.get_or_404(employee_id)
    data = request.json
    p = Performance(
        employee_id=employee_id,
        metric=data.get('metric'),
        value=data.get('value'),
        date=data.get('date')
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'message': 'Performance added', 'id': p.id}), 201

@employee_bp.route('/employees/<int:employee_id>/performances/<int:perf_id>', methods=['PUT'])
def update_performance(employee_id, perf_id):
    p = Performance.query.get_or_404(perf_id)
    data = request.json
    p.metric = data.get('metric', p.metric)
    p.value = data.get('value', p.value)
    p.date = data.get('date', p.date)
    db.session.commit()
    return jsonify({'message': 'Performance updated'})

@employee_bp.route('/employees/<int:employee_id>/performances/<int:perf_id>', methods=['DELETE'])
def delete_performance(employee_id, perf_id):
    p = Performance.query.get_or_404(perf_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Performance deleted'})
