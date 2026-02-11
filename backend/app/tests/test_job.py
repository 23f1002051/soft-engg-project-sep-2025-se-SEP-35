import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import Job


class TestJobRoutes:
    """Critical Test Suite for Job Management APIs - Top 10 Test Cases"""
    
    # ==================== TEST 1: GET ALL JOBS ====================
    
    def test_01_get_all_jobs_success(self):
        """TC_JOB_001: Get all jobs - Success with multiple jobs"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Get All Jobs - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create multiple jobs
            job1 = Job(
                title='Senior Python Developer',
                description='Looking for experienced Python developer',
                company='Tech Corp India',
                location='Bangalore',
                type='Full-time',
                salary='₹15-20 LPA',
                tags='Python,Django,Flask'
            )
            job2 = Job(
                title='Data Scientist',
                description='ML and AI expert needed',
                company='AI Solutions',
                location='Mumbai',
                type='Full-time',
                salary='₹18-25 LPA',
                tags='Python,ML,AI'
            )
            db.session.add_all([job1, job2])
            db.session.commit()
            
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/jobs")
            print(f"Input: None")
            
            response = client.get('/api/jobs')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: List of 2 jobs")
            print(f"Actual Output: {len(result)} jobs returned")
            
            assert response.status_code == 200
            assert isinstance(result, list)
            assert len(result) == 2
            
            titles = [job['title'] for job in result]
            assert 'Senior Python Developer' in titles
            assert 'Data Scientist' in titles
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 2: GET SINGLE JOB ====================
    
    def test_02_get_job_by_id_success(self):
        """TC_JOB_002: Get single job by ID - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Get Job by ID - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            job = Job(
                title='Full Stack Developer',
                description='React and Node.js expert',
                company='Startup Hub',
                location='Hyderabad',
                type='Full-time',
                salary='₹12-18 LPA',
                tags='React,Node.js,MongoDB'
            )
            db.session.add(job)
            db.session.commit()
            
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/jobs/1")
            print(f"Input: job_id = 1")
            
            response = client.get('/api/jobs/1')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Job details with all fields")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['title'] == 'Full Stack Developer'
            assert result['company'] == 'Startup Hub'
            assert result['location'] == 'Hyderabad'
            assert result['salary'] == '₹12-18 LPA'
            assert result['tags'] == 'React,Node.js,MongoDB'
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 3: GET NON-EXISTENT JOB ====================
    
    def test_03_get_job_nonexistent(self):
        """TC_JOB_003: Get job with invalid ID - 404 Error"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Get Job - Non-existent ID")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/jobs/999")
            print(f"Input: job_id = 999 (doesn't exist)")
            
            response = client.get('/api/jobs/999')
            
            print(f"Expected Status Code: 404")
            print(f"Actual Status Code: {response.status_code}")
            
            assert response.status_code == 404
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 4: CREATE JOB SUCCESS ====================
    
    def test_04_create_job_success(self):
        """TC_JOB_004: Create new job - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Create Job - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            data = {
                "title": "DevOps Engineer",
                "description": "AWS and Kubernetes expert needed",
                "company": "Cloud Solutions Ltd",
                "location": "Pune",
                "type": "Full-time",
                "salary": "₹16-22 LPA",
                "tags": "AWS,Kubernetes,Docker,CI/CD"
            }
            
            print(f"API Being Tested: POST /api/jobs")
            print(f"Input: {data}")
            
            response = client.post('/api/jobs', json=data)
            result = response.get_json()
            
            print(f"Expected Status Code: 201")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Job created with ID")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 201
            assert result['message'] == 'Job created'
            assert 'id' in result
            
            # Verify job was created
            job = Job.query.get(result['id'])
            assert job is not None
            assert job.title == 'DevOps Engineer'
            assert job.company == 'Cloud Solutions Ltd'
            assert job.tags == 'AWS,Kubernetes,Docker,CI/CD'
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 5: CREATE JOB WITH PARTIAL DATA ====================
    
    def test_05_create_job_partial_data(self):
        """TC_JOB_005: Create job with only required fields"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Create Job - Partial Data (Required Fields Only)")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            data = {
                "title": "Software Tester",
                "description": "Manual and automation testing",
                "company": "QA Tech"
                # Missing: location, type, salary, tags
            }
            
            print(f"API Being Tested: POST /api/jobs")
            print(f"Input: {data} (partial data)")
            
            response = client.post('/api/jobs', json=data)
            result = response.get_json()
            
            print(f"Expected Status Code: 201")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Job created with NULL optional fields")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 201
            assert result['message'] == 'Job created'
            
            # Verify job with NULL fields
            job = Job.query.get(result['id'])
            assert job.title == 'Software Tester'
            assert job.location is None
            assert job.salary is None
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 6: UPDATE JOB SUCCESS ====================
    
    def test_06_update_job_success(self):
        """TC_JOB_006: Update existing job - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 6: Update Job - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create initial job
            job = Job(
                title='Junior Developer',
                description='Entry level position',
                company='Tech Startup',
                location='Bangalore',
                type='Full-time',
                salary='₹5-8 LPA',
                tags='Java,Spring'
            )
            db.session.add(job)
            db.session.commit()
            
            client = app.test_client()
            
            # Update job
            update_data = {
                "title": "Senior Developer",
                "salary": "₹15-20 LPA",
                "tags": "Java,Spring,Microservices,AWS"
            }
            
            print(f"API Being Tested: PUT /api/jobs/1")
            print(f"Input: {update_data}")
            
            response = client.put('/api/jobs/1', json=update_data)
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Job updated")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['message'] == 'Job updated'
            
            # Verify updates
            verify_response = client.get('/api/jobs/1')
            verify_result = verify_response.get_json()
            assert verify_result['title'] == 'Senior Developer'
            assert verify_result['salary'] == '₹15-20 LPA'
            assert verify_result['tags'] == 'Java,Spring,Microservices,AWS'
            # Unchanged fields
            assert verify_result['company'] == 'Tech Startup'
            assert verify_result['location'] == 'Bangalore'
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 7: UPDATE NON-EXISTENT JOB ====================
    
    def test_07_update_job_nonexistent(self):
        """TC_JOB_007: Update non-existent job - 404 Error"""
        
        print("\n" + "="*70)
        print("TEST CASE 7: Update Job - Non-existent ID")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            data = {
                "title": "Updated Title",
                "salary": "₹20 LPA"
            }
            
            print(f"API Being Tested: PUT /api/jobs/999")
            print(f"Input: {data}")
            
            response = client.put('/api/jobs/999', json=data)
            
            print(f"Expected Status Code: 404")
            print(f"Actual Status Code: {response.status_code}")
            
            assert response.status_code == 404
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 8: DELETE JOB SUCCESS ====================
    
    def test_08_delete_job_success(self):
        """TC_JOB_008: Delete existing job - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 8: Delete Job - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create job to delete
            job = Job(
                title='Temporary Position',
                description='Short term contract',
                company='Contract Corp',
                location='Remote',
                type='Contract',
                salary='₹10 LPA',
                tags='Python'
            )
            db.session.add(job)
            db.session.commit()
            
            client = app.test_client()
            
            print(f"API Being Tested: DELETE /api/jobs/1")
            print(f"Input: job_id = 1")
            
            response = client.delete('/api/jobs/1')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Job deleted")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['message'] == 'Job deleted'
            
            # Verify deletion
            verify_response = client.get('/api/jobs/1')
            assert verify_response.status_code == 404
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 9: DELETE NON-EXISTENT JOB ====================
    
    def test_09_delete_job_nonexistent(self):
        """TC_JOB_009: Delete non-existent job - 404 Error"""
        
        print("\n" + "="*70)
        print("TEST CASE 9: Delete Job - Non-existent ID")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            print(f"API Being Tested: DELETE /api/jobs/999")
            print(f"Input: job_id = 999 (doesn't exist)")
            
            response = client.delete('/api/jobs/999')
            
            print(f"Expected Status Code: 404")
            print(f"Actual Status Code: {response.status_code}")
            
            assert response.status_code == 404
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 10: GET EMPTY JOB LIST ====================
    
    def test_10_get_all_jobs_empty(self):
        """TC_JOB_010: Get all jobs when database is empty"""
        
        print("\n" + "="*70)
        print("TEST CASE 10: Get All Jobs - Empty Database")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/jobs")
            print(f"Input: None (empty database)")
            
            response = client.get('/api/jobs')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Empty array []")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert isinstance(result, list)
            assert len(result) == 0
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
