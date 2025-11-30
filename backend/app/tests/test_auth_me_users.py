
import pytest
import sys
import os
import jwt
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import User, Employee
from app.models.profile import Profile

@pytest.fixture
def client():
    """Create test client with test users"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Create test candidate user
        user1 = User(
            first_name='Rahul',
            last_name='Sharma',
            email='rahul.sharma@jobportal.in',
            role='candidate'
        )
        user1.set_password('Candidate@123')
        db.session.add(user1)
        db.session.commit()
        
        profile1 = Profile(user_id=user1.id, phone='9876543210')
        db.session.add(profile1)
        
        # Create test HR user
        user2 = User(
            first_name='Deepika',
            last_name='Menon',
            company_name='InfoTech Solutions',
            email='deepika.hr@infotech.co.in',
            role='hr'
        )
        user2.set_password('HRSecure@456')
        db.session.add(user2)
        db.session.commit()
        
        profile2 = Profile(user_id=user2.id, phone='8765432109')
        db.session.add(profile2)
        
        # Create another candidate
        user3 = User(
            first_name='Arjun',
            last_name='Reddy',
            email='arjun.reddy@careers.net',
            role='candidate'
        )
        user3.set_password('Secure@789')
        db.session.add(user3)
        db.session.commit()
        
        profile3 = Profile(user_id=user3.id, phone='7654321098')
        db.session.add(profile3)
        
        # Create employee record for user1
        employee = Employee(user_id=str(user1.id), department='Software Development')
        db.session.add(employee)
        
        db.session.commit()
        
        # Generate valid token for user1
        token = jwt.encode({
            'user_id': user1.id,
            'role': user1.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        app.test_token = token
        app.test_user_id = user1.id
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()


class TestAuthMe:
    """Test Suite for GET /api/auth/me"""
    
    def test_01_get_current_user_valid_token(self, client):
        """TC_ME_001: Get current user with valid JWT token"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Get Current User with Valid Token")
        print("="*70)
        
        # Get the token from fixture
        from app import create_app
        app = create_app()
        
        with app.app_context():
            user = User.query.filter_by(email='rahul.sharma@jobportal.in').first()
            token = jwt.encode({
                'user_id': user.id,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
        
        headers = {'Authorization': f'Bearer {token}'}
        
        print(f"API Being Tested: GET /api/auth/me")
        print(f"Input: Authorization Header with valid JWT")
        
        response = client.get('/api/auth/me', headers=headers)
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: User details (id, first_name, last_name, email, role)")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 200
        assert result['first_name'] == 'Rahul'
        assert result['last_name'] == 'Sharma'
        assert result['email'] == 'rahul.sharma@jobportal.in'
        assert result['role'] == 'candidate'
        assert 'id' in result
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_02_get_current_user_missing_token(self, client):
        """TC_ME_002: Get current user without Authorization header"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Get Current User without Token")
        print("="*70)
        
        print(f"API Being Tested: GET /api/auth/me")
        print(f"Input: No Authorization header")
        
        response = client.get('/api/auth/me')
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Missing or invalid token'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Missing or invalid token'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_03_get_current_user_invalid_token(self, client):
        """TC_ME_003: Get current user with invalid/malformed token"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Get Current User with Invalid Token")
        print("="*70)
        
        headers = {'Authorization': 'Bearer invalid.jwt.token.malformed'}
        
        print(f"API Being Tested: GET /api/auth/me")
        print(f"Input: Authorization Header with invalid JWT")
        
        response = client.get('/api/auth/me', headers=headers)
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Invalid token'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Invalid token'
        
        print("✅ TEST PASSED")
        print("="*70)


class TestUsersBasic:
    """Test Suite for GET /api/auth/users/basic"""
    
    def test_04_get_users_basic_returns_only_candidates(self, client):
        """TC_USERS_001: Get users/basic returns only candidates"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Get Users Basic - Only Candidates")
        print("="*70)
        
        print(f"API Being Tested: GET /api/auth/users/basic")
        print(f"Input: None (GET request)")
        
        response = client.get('/api/auth/users/basic')
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: List of users with role='candidate' only")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 200
        assert isinstance(result, list)
        assert len(result) == 2  # Only 2 candidates (Rahul and Arjun)
        
        # Verify all returned users are candidates
        emails = [user['email'] for user in result]
        assert 'rahul.sharma@jobportal.in' in emails
        assert 'arjun.reddy@careers.net' in emails
        assert 'deepika.hr@infotech.co.in' not in emails  # HR user should not be included
        
        # Verify structure
        for user in result:
            assert 'id' in user
            assert 'first_name' in user
            assert 'last_name' in user
            assert 'email' in user
            assert 'phone' in user
            assert 'employee_id' in user
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_05_get_users_basic_includes_employee_id(self, client):
        """TC_USERS_002: Get users/basic includes employee_id when exists"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Get Users Basic - Employee ID Mapping")
        print("="*70)
        
        print(f"API Being Tested: GET /api/auth/users/basic")
        print(f"Input: None (GET request)")
        
        response = client.get('/api/auth/users/basic')
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected: Rahul has employee_id, Arjun has None")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 200
        
        # Find Rahul and Arjun in results
        rahul = next((u for u in result if u['email'] == 'rahul.sharma@jobportal.in'), None)
        arjun = next((u for u in result if u['email'] == 'arjun.reddy@careers.net'), None)
        
        assert rahul is not None
        assert arjun is not None
        
        # Rahul should have employee_id (we created Employee record for him)
        assert rahul['employee_id'] is not None
        assert rahul['phone'] == '9876543210'
        
        # Arjun should not have employee_id
        assert arjun['employee_id'] is None
        assert arjun['phone'] == '7654321098'
        
        print("✅ TEST PASSED")
        print("="*70)
