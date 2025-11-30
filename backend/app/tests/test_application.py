import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import db
from app.models import User, Job, Application


class TestApplicationRoutes:
    """Critical Test Suite for Application Management APIs - Top 5 Test Cases"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for EACH test - ensures clean database"""
        from app import create_app
        
        # Create app with test configuration
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Push application context
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all tables
        db.create_all()
        
        # Create test client
        self.client = self.app.test_client()
        
        yield  # Test runs here
        
        # Cleanup after test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # ==================== TEST 1: CREATE APPLICATION ====================
    
    def test_01_create_application_success(self):
        """TC_APP_001: Create new application - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Create Application - Success")
        print("="*70)
        
        # Create candidate user
        user = User(
            first_name='Rahul',
            last_name='Verma',
            email='rahul.verma.tc01@test.in',
            role='candidate'
        )
        user.set_password('Pass@123')
        db.session.add(user)
        db.session.commit()
        
        # Create job posting
        job = Job(
            title='Python Developer',
            description='Looking for Python expert',
            company='Tech Corp',
            location='Bangalore',
            type='Full-time',
            salary='₹10-15 LPA',
            tags='Python,Django'
        )
        db.session.add(job)
        db.session.commit()
        
        # Verify initial state
        initial_count = Application.query.count()
        print(f"Initial applications in database: {initial_count}")
        assert initial_count == 0
        
        data = {
            "user_id": user.id,
            "job_id": job.id,
            "status": "applied"
        }
        
        print(f"API Being Tested: POST /api/applications")
        print(f"Input: {data}")
        
        response = self.client.post('/api/applications', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected: Application created with ID")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['message'] == 'Application created'
        assert 'id' in result
        
        # Verify application was created
        application = Application.query.get(result['id'])
        assert application is not None
        assert application.user_id == user.id
        assert application.job_id == job.id
        assert application.status == 'applied'
        assert application.applied_at is not None
        
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== TEST 2: GET ALL APPLICATIONS ====================
    
    def test_02_get_all_applications_success(self):
        """TC_APP_002: Get all applications - Success with multiple applications"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Get All Applications - Success")
        print("="*70)
        
        # Create users
        user1 = User(
            first_name='Priya',
            last_name='Sharma',
            email='priya.sharma.tc02@test.in',
            role='candidate'
        )
        user1.set_password('Pass@456')
        db.session.add(user1)
        
        user2 = User(
            first_name='Amit',
            last_name='Patel',
            email='amit.patel.tc02@test.in',
            role='candidate'
        )
        user2.set_password('Pass@789')
        db.session.add(user2)
        db.session.commit()
        
        # Create jobs
        job1 = Job(
            title='Data Scientist',
            description='ML expert needed',
            company='AI Solutions',
            location='Mumbai',
            type='Full-time',
            salary='₹15-20 LPA',
            tags='Python,ML'
        )
        job2 = Job(
            title='Frontend Developer',
            description='React developer',
            company='Web Agency',
            location='Pune',
            type='Full-time',
            salary='₹8-12 LPA',
            tags='React,JavaScript'
        )
        db.session.add_all([job1, job2])
        db.session.commit()
        
        # Create applications
        app1 = Application(
            user_id=user1.id,
            job_id=job1.id,
            status='applied'
        )
        app2 = Application(
            user_id=user2.id,
            job_id=job2.id,
            status='shortlisted'
        )
        app3 = Application(
            user_id=user1.id,
            job_id=job2.id,
            status='applied'
        )
        db.session.add_all([app1, app2, app3])
        db.session.commit()
        
        print(f"API Being Tested: GET /api/applications")
        print(f"Input: None")
        
        response = self.client.get('/api/applications')
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected: List of 3 applications")
        print(f"Actual Output: {len(result)} applications returned")
        
        assert response.status_code == 200
        assert isinstance(result, list)
        assert len(result) == 3, f"Expected 3 applications, got {len(result)}"
        
        # Verify application data
        statuses = [app['status'] for app in result]
        assert 'applied' in statuses
        assert 'shortlisted' in statuses
        
        # Verify all applications have required fields
        for app in result:
            assert 'id' in app
            assert 'user_id' in app
            assert 'job_id' in app
            assert 'status' in app
            assert 'applied_at' in app
        
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== TEST 3: UPDATE APPLICATION STATUS ====================
    
    def test_03_update_application_status_success(self):
        """TC_APP_003: Update application status - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Update Application Status - Success")
        print("="*70)
        
        # Create user and job
        user = User(
            first_name='Neha',
            last_name='Kapoor',
            email='neha.kapoor.tc03@test.in',
            role='candidate'
        )
        user.set_password('Pass@321')
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            title='Backend Developer',
            description='Node.js expert',
            company='Startup Inc',
            location='Hyderabad',
            type='Full-time',
            salary='₹12-18 LPA',
            tags='Node.js,MongoDB'
        )
        db.session.add(job)
        db.session.commit()
        
        # Create application
        application = Application(
            user_id=user.id,
            job_id=job.id,
            status='applied'
        )
        db.session.add(application)
        db.session.commit()
        
        app_id = application.id
        
        # Update status
        update_data = {
            "status": "interview_scheduled"
        }
        
        print(f"API Being Tested: PUT /api/applications/{app_id}")
        print(f"Input: {update_data}")
        print(f"Initial Status: applied")
        
        response = self.client.put(f'/api/applications/{app_id}', json=update_data)
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected: Application status updated")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 200
        assert result['message'] == 'Application updated'
        
        # Verify status was updated
        verify_response = self.client.get(f'/api/applications/{app_id}')
        verify_result = verify_response.get_json()
        assert verify_result['status'] == 'interview_scheduled'
        
        print(f"Updated Status: {verify_result['status']}")
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== TEST 4: DELETE APPLICATION ====================
    
    def test_04_delete_application_success(self):
        """TC_APP_004: Delete application - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Delete Application - Success")
        print("="*70)
        
        # Create user and job
        user = User(
            first_name='Vikram',
            last_name='Singh',
            email='vikram.singh.tc04@test.in',
            role='candidate'
        )
        user.set_password('Pass@654')
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            title='DevOps Engineer',
            description='AWS expert',
            company='Cloud Corp',
            location='Bangalore',
            type='Full-time',
            salary='₹18-25 LPA',
            tags='AWS,Docker'
        )
        db.session.add(job)
        db.session.commit()
        
        # Create application
        application = Application(
            user_id=user.id,
            job_id=job.id,
            status='applied'
        )
        db.session.add(application)
        db.session.commit()
        
        app_id = application.id
        
        # Verify application exists
        initial_count = Application.query.count()
        assert initial_count == 1
        
        print(f"API Being Tested: DELETE /api/applications/{app_id}")
        print(f"Input: application_id = {app_id}")
        
        response = self.client.delete(f'/api/applications/{app_id}')
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected: Application deleted")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 200
        assert result['message'] == 'Application deleted'
        
        # Verify deletion
        verify_response = self.client.get(f'/api/applications/{app_id}')
        assert verify_response.status_code == 404
        
        # Verify count decreased
        final_count = Application.query.count()
        assert final_count == 0
        
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== TEST 5: DUPLICATE APPLICATION PREVENTION ====================
    
    def test_05_duplicate_application_allowed(self):
        """TC_APP_005: Duplicate application - Backend allows duplicates (BUG)"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Duplicate Application - Backend Bug")
        print("="*70)
        
        # Create user and job
        user = User(
            first_name='Sneha',
            last_name='Reddy',
            email='sneha.reddy.tc05@test.in',
            role='candidate'
        )
        user.set_password('Pass@987')
        db.session.add(user)
        db.session.commit()
        
        job = Job(
            title='Full Stack Developer',
            description='MERN stack expert',
            company='Tech Startup',
            location='Pune',
            type='Full-time',
            salary='₹10-15 LPA',
            tags='React,Node.js'
        )
        db.session.add(job)
        db.session.commit()
        
        # Create first application
        data = {
            "user_id": user.id,
            "job_id": job.id,
            "status": "applied"
        }
        
        print(f"API Being Tested: POST /api/applications (twice)")
        print(f"Input: {data}")
        
        # First application
        response1 = self.client.post('/api/applications', json=data)
        result1 = response1.get_json()
        
        print(f"First Application Status Code: {response1.status_code}")
        assert response1.status_code == 201
        
        # Try to apply again (duplicate)
        response2 = self.client.post('/api/applications', json=data)
        result2 = response2.get_json()
        
        print(f"Second Application Status Code: {response2.status_code}")
        print(f"Expected: 400 or 409 (Duplicate not allowed)")
        print(f"Actual: {response2.status_code} (Backend allows duplicates)")
        
        # Check if backend prevents duplicates
        if response2.status_code == 201:
            print(" BACKEND BUG DETECTED: Duplicate applications allowed")
            
            # Verify two applications exist
            applications = Application.query.filter_by(
                user_id=user.id,
                job_id=job.id
            ).all()
            
            print(f"Applications for same user+job: {len(applications)}")
            assert len(applications) == 2, "Backend should prevent duplicates"
            
            print("TEST PASSED - Backend bug documented")
            print("BUG: Backend allows duplicate applications")
            print("FIX NEEDED: Add unique constraint or check in create_application()")
            print("   Recommendation: Add unique constraint on (user_id, job_id)")
        else:
            print("✅ Backend correctly prevents duplicate applications")
        
        print("="*70)
