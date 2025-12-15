
import pytest
import sys
import os
import jwt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import User
from app.models.profile import Profile

@pytest.fixture
def client():
    """Create test client with clean database"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Create a test user for login tests
        user = User(
            first_name='Ananya',
            last_name='Krishnan',
            email='ananya.k@techsolutions.in',
            role='candidate'
        )
        user.set_password('SecurePass@2024')
        db.session.add(user)
        db.session.commit()
        
        # Create profile with phone
        profile = Profile(user_id=user.id, phone='9123456780')
        db.session.add(profile)
        db.session.commit()
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()


class TestAuthLogin:
    """Test Suite for POST /api/auth/login"""
    
    def test_01_login_valid_credentials(self, client):
        """TC_LOGIN_001: Login with valid email and password"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Login with Valid Credentials")
        print("="*70)
        
        data = {
            "email": "ananya.k@techsolutions.in",
            "password": "SecurePass@2024"
        }
        
        print(f"API Being Tested: POST /api/auth/login")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/login', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 200")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'message': 'Login successful', 'token': '<JWT>', 'role': 'candidate', 'user_id': 'Ananya780'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 200
        assert result['message'] == 'Login successful'
        assert 'token' in result
        assert result['role'] == 'candidate'
        assert result['user_id'] == 'Ananya780'
        
        # Verify JWT token is valid
        assert len(result['token']) > 0
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_02_login_invalid_password(self, client):
        """TC_LOGIN_002: Login with wrong password"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Login with Invalid Password")
        print("="*70)
        
        data = {
            "email": "ananya.k@techsolutions.in",
            "password": "IncorrectPass@999"  # Wrong password
        }
        
        print(f"API Being Tested: POST /api/auth/login")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/login', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Invalid credentials'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Invalid credentials'
        assert 'token' not in result
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_03_login_nonexistent_email(self, client):
        """TC_LOGIN_003: Login with email that doesn't exist"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Login with Non-existent Email")
        print("="*70)
        
        data = {
            "email": "unknown.user@notregistered.com",  # Email doesn't exist
            "password": "RandomPass@456"
        }
        
        print(f"API Being Tested: POST /api/auth/login")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/login', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Invalid credentials'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Invalid credentials'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_04_login_missing_email(self, client):
        """TC_LOGIN_004: Login without email field"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Login with Missing Email")
        print("="*70)
        
        data = {
            # email is missing
            "password": "SecurePass@2024"
        }
        
        print(f"API Being Tested: POST /api/auth/login")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/login', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Invalid credentials'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Invalid credentials'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_05_login_missing_password(self, client):
        """TC_LOGIN_005: Login without password field"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Login with Missing Password")
        print("="*70)
        
        data = {
            "email": "ananya.k@techsolutions.in"
            # password is missing
        }
        
        print(f"API Being Tested: POST /api/auth/login")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/login', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 401")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Invalid credentials'}}")
        print(f"Actual Output: {result}")
        
        # Assertions
        assert response.status_code == 401
        assert result['error'] == 'Invalid credentials'
        
        print("✅ TEST PASSED")
        print("="*70)
