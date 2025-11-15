from flask import Blueprint, request, jsonify
from ..database import db
from ..models import Job

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'company': job.company,
        'location': job.location,
        'type': job.type,
        'salary': job.salary,
        'tags': job.tags,
        'created_at': job.created_at
    } for job in jobs])

@job_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'company': job.company,
        'location': job.location,
        'type': job.type,
        'salary': job.salary,
        'tags': job.tags,
        'created_at': job.created_at
    })

@job_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    job = Job(
        title=data.get('title'),
        description=data.get('description'),
        company=data.get('company'),
        location=data.get('location'),
        type=data.get('type'),
        salary=data.get('salary'),
        tags=data.get('tags')
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({'message': 'Job created', 'id': job.id}), 201

@job_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.company = data.get('company', job.company)
    job.location = data.get('location', job.location)
    job.type = data.get('type', job.type)
    job.salary = data.get('salary', job.salary)
    job.tags = data.get('tags', job.tags)
    db.session.commit()
    return jsonify({'message': 'Job updated'})

@job_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'})
