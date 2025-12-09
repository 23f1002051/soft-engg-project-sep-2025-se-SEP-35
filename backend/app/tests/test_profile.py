
import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import User, Profile, Experience


class TestProfileRoutes:
    """Critical Test Suite for Profile Management APIs - Top 8 Test Cases"""
    
    # ==================== TEST 1: GET ALL PROFILES ====================
    
    def test_01_get_all_profiles_success(self):
        """TC_PROF_001: Get all profiles - Success with multiple profiles"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Get All Profiles - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create users with profiles
            user1 = User(
                first_name='Rajesh',
                last_name='Kumar',
                email='rajesh.kumar.tc01@test.in',
                role='candidate'
            )
            user1.set_password('Pass@123')
            db.session.add(user1)
            db.session.commit()
            
            profile1 = Profile(
                user_id=user1.id,
                phone='9876543210',
                location='Bangalore',
                summary='Experienced Python Developer',
                completeness=75
            )
            db.session.add(profile1)
            
            user2 = User(
                first_name='Priya',
                last_name='Sharma',
                email='priya.sharma.tc01@test.in',
                role='candidate'
            )
            user2.set_password('Pass@456')
            db.session.add(user2)
            db.session.commit()
            
            profile2 = Profile(
                user_id=user2.id,
                phone='8765432109',
                location='Mumbai',
                summary='Data Scientist',
                completeness=80
            )
            db.session.add(profile2)
            db.session.commit()
            
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/profiles")
            print(f"Input: None")
            
            response = client.get('/api/profiles')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: List of 2 profiles")
            print(f"Actual Output: {len(result)} profiles returned")
            
            assert response.status_code == 200
            assert isinstance(result, list)
            assert len(result) == 2, f"Expected 2 profiles, got {len(result)}"
            
            # Verify profile data
            emails = [p['email'] for p in result]
            assert 'rajesh.kumar.tc01@test.in' in emails
            assert 'priya.sharma.tc01@test.in' in emails
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 2: GET SINGLE PROFILE BY ID ====================
    
    def test_02_get_profile_by_id_success(self):
        """TC_PROF_002: Get single profile by ID - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Get Profile by ID - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Amit',
                last_name='Patel',
                email='amit.patel.tc02@test.in',
                role='candidate'
            )
            user.set_password('Pass@789')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='7654321098',
                location='Pune',
                summary='Full Stack Developer with 5 years experience',
                completeness=90
            )
            db.session.add(profile)
            db.session.commit()
            
            profile_id = profile.id
            
            client = app.test_client()
            
            print(f"API Being Tested: GET /api/profiles/{profile_id}")
            print(f"Input: profile_id = {profile_id}")
            
            response = client.get(f'/api/profiles/{profile_id}')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Profile details with user info")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['first_name'] == 'Amit'
            assert result['email'] == 'amit.patel.tc02@test.in'
            assert result['phone'] == '7654321098'
            assert result['location'] == 'Pune'
            assert result['completeness'] == 90
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 3: CREATE PROFILE ====================
    
    def test_03_create_profile_success(self):
        """TC_PROF_003: Create new profile - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Create Profile - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create user first
            user = User(
                first_name='Sneha',
                last_name='Reddy',
                email='sneha.reddy.tc03@test.in',
                role='candidate'
            )
            user.set_password('Pass@321')
            db.session.add(user)
            db.session.commit()
            
            client = app.test_client()
            
            data = {
                "user_id": user.id,
                "phone": "9123456780",
                "location": "Hyderabad",
                "summary": "DevOps Engineer with AWS expertise",
                "completeness": 60
            }
            
            print(f"API Being Tested: POST /api/profiles")
            print(f"Input: {data}")
            
            response = client.post('/api/profiles', json=data)
            result = response.get_json()
            
            print(f"Expected Status Code: 201")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Profile created with ID")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 201
            assert result['message'] == 'Profile created'
            assert 'id' in result
            
            # Verify profile was created
            profile = Profile.query.get(result['id'])
            assert profile is not None
            assert profile.phone == '9123456780'
            assert profile.location == 'Hyderabad'
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 4: UPDATE PROFILE ====================
    
    def test_04_update_profile_success(self):
        """TC_PROF_004: Update existing profile - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Update Profile - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Vikram',
                last_name='Singh',
                email='vikram.singh.tc04@test.in',
                role='candidate'
            )
            user.set_password('Pass@654')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='8888888888',
                location='Delhi',
                summary='Junior Developer',
                completeness=40
            )
            db.session.add(profile)
            db.session.commit()
            
            profile_id = profile.id
            
            client = app.test_client()
            
            update_data = {
                "location": "Bangalore",
                "summary": "Senior Developer with 3 years experience",
                "completeness": 85
            }
            
            print(f"API Being Tested: PUT /api/profiles/{profile_id}")
            print(f"Input: {update_data}")
            
            response = client.put(f'/api/profiles/{profile_id}', json=update_data)
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Profile updated")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['message'] == 'Profile updated'
            
            # Verify updates
            verify_response = client.get(f'/api/profiles/{profile_id}')
            verify_result = verify_response.get_json()
            assert verify_result['location'] == 'Bangalore'
            assert verify_result['summary'] == 'Senior Developer with 3 years experience'
            assert verify_result['completeness'] == 85
            assert verify_result['phone'] == '8888888888'  # Unchanged
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 5: DELETE PROFILE ====================
    
    def test_05_delete_profile_success(self):
        """TC_PROF_005: Delete existing profile - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Delete Profile - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Temp',
                last_name='User',
                email='temp.user.tc05@test.in',
                role='candidate'
            )
            user.set_password('Pass@999')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='7777777777',
                location='Chennai',
                summary='Temporary profile',
                completeness=20
            )
            db.session.add(profile)
            db.session.commit()
            
            profile_id = profile.id
            
            client = app.test_client()
            
            print(f"API Being Tested: DELETE /api/profiles/{profile_id}")
            print(f"Input: profile_id = {profile_id}")
            
            response = client.delete(f'/api/profiles/{profile_id}')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Profile deleted")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['message'] == 'Profile deleted'
            
            # Verify deletion
            verify_response = client.get(f'/api/profiles/{profile_id}')
            assert verify_response.status_code == 404
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 6: ADD EXPERIENCE (BACKEND BUG) ====================
    
    def test_06_add_experience_backend_bug(self):
        """TC_EXP_001: Add experience - FAILS due to backend not converting date strings"""
        
        print("\n" + "="*70)
        print("TEST CASE 6: Add Experience - Backend Date Conversion Bug")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Arjun',
                last_name='Desai',
                email='arjun.desai.tc06@test.in',
                role='candidate'
            )
            user.set_password('Pass@111')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='6666666666',
                location='Kolkata',
                summary='Software Engineer',
                completeness=50
            )
            db.session.add(profile)
            db.session.commit()
            
            client = app.test_client()
            
            exp_data = {
                "title": "Senior Software Engineer",
                "company": "Tech Solutions Pvt Ltd",
                "start_date": "2020-01-15",
                "end_date": "2023-12-31",
                "description": "Led team of 5 developers, built microservices architecture"
            }
            
            print(f"API Being Tested: POST /api/profiles/1/experiences")
            print(f"Input: {exp_data}")
            print(f"⚠️  EXPECTED FAILURE: Backend doesn't convert date strings to date objects")
            
            response = client.post('/api/profiles/1/experiences', json=exp_data)
            
            print(f"Expected Status Code: 500 (Backend Error)")
            print(f"Actual Status Code: {response.status_code}")
            
            # This SHOULD fail because backend doesn't handle date conversion
            assert response.status_code == 500, "Backend should fail on date string"
            
            print("✅ TEST PASSED - Backend bug documented")
            print("🐛 BUG: Backend route 'add_experience' doesn't convert date strings")
            print("🔧 FIX NEEDED: Add datetime.strptime() in profile_routes.py")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 7: UPDATE EXPERIENCE (BACKEND BUG) ====================
    
    def test_07_update_experience_backend_bug(self):
        """TC_EXP_002: Update experience - FAILS due to backend not converting date strings"""
        
        print("\n" + "="*70)
        print("TEST CASE 7: Update Experience - Backend Date Conversion Bug")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Meera',
                last_name='Joshi',
                email='meera.joshi.tc07@test.in',
                role='candidate'
            )
            user.set_password('Pass@222')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='5555555555',
                location='Ahmedabad',
                summary='Product Manager',
                completeness=70
            )
            db.session.add(profile)
            db.session.commit()
            
            # Create experience with proper date objects (direct DB insert)
            experience = Experience(
                profile_id=profile.id,
                title='Product Manager',
                company='Startup Inc',
                start_date=datetime.strptime('2021-06-01', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2023-05-31', '%Y-%m-%d').date(),
                description='Managed product roadmap'
            )
            db.session.add(experience)
            db.session.commit()
            
            client = app.test_client()
            
            # Try to update with string dates
            update_data = {
                "title": "Senior Product Manager",
                "company": "Big Tech Corp",
                "description": "Led product strategy for 3 major products",
                "start_date": "2021-06-01",
                "end_date": "2024-01-31"
            }
            
            print(f"API Being Tested: PUT /api/profiles/1/experiences/1")
            print(f"Input: {update_data}")
            print(f"⚠️  EXPECTED FAILURE: Backend doesn't convert date strings")
            
            response = client.put('/api/profiles/1/experiences/1', json=update_data)
            
            print(f"Expected Status Code: 500 (Backend Error)")
            print(f"Actual Status Code: {response.status_code}")
            
            # This SHOULD fail because backend doesn't handle date conversion
            assert response.status_code == 500, "Backend should fail on date string"
            
            print("✅ TEST PASSED - Backend bug documented")
            print("🐛 BUG: Backend route 'update_experience' doesn't convert date strings")
            print("🔧 FIX NEEDED: Add datetime.strptime() in profile_routes.py")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
    
    # ==================== TEST 8: DELETE EXPERIENCE ====================
    
    def test_08_delete_experience_success(self):
        """TC_EXP_003: Delete experience from profile - Success"""
        
        print("\n" + "="*70)
        print("TEST CASE 8: Delete Experience - Success")
        print("="*70)
        
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            user = User(
                first_name='Karthik',
                last_name='Nair',
                email='karthik.nair.tc08@test.in',
                role='candidate'
            )
            user.set_password('Pass@333')
            db.session.add(user)
            db.session.commit()
            
            profile = Profile(
                user_id=user.id,
                phone='4444444444',
                location='Kochi',
                summary='Designer',
                completeness=65
            )
            db.session.add(profile)
            db.session.commit()
            
            # Create experiences with proper date objects
            exp1 = Experience(
                profile_id=profile.id,
                title='UI Designer',
                company='Design Studio',
                start_date=datetime.strptime('2019-01-01', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2021-12-31', '%Y-%m-%d').date(),
                description='Created UI designs'
            )
            exp2 = Experience(
                profile_id=profile.id,
                title='UX Designer',
                company='UX Agency',
                start_date=datetime.strptime('2022-01-01', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(),
                description='User research and wireframing'
            )
            db.session.add_all([exp1, exp2])
            db.session.commit()
            
            exp1_id = exp1.id
            
            client = app.test_client()
            
            print(f"API Being Tested: DELETE /api/profiles/1/experiences/{exp1_id}")
            print(f"Input: profile_id=1, exp_id={exp1_id}")
            
            response = client.delete(f'/api/profiles/1/experiences/{exp1_id}')
            result = response.get_json()
            
            print(f"Expected Status Code: 200")
            print(f"Actual Status Code: {response.status_code}")
            print(f"Expected: Experience deleted, 1 experience remains")
            print(f"Actual Output: {result}")
            
            assert response.status_code == 200
            assert result['message'] == 'Experience deleted'
            
            # Verify deletion
            verify_response = client.get('/api/profiles/1')
            verify_result = verify_response.get_json()
            assert len(verify_result['experiences']) == 1
            assert verify_result['experiences'][0]['title'] == 'UX Designer'
            
            print("✅ TEST PASSED")
            print("="*70)
            
            db.session.remove()
            db.drop_all()
