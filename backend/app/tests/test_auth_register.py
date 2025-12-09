
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db

@pytest.fixture
def client():
    """Create test client with clean database"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


class TestAuthRegister:
    """Test Suite for POST /api/auth/register"""
    
    # ==================== POSITIVE TEST CASES ====================
    
    def test_01_register_valid_candidate(self, client):
        """TC_REG_001: Register with valid candidate data"""
        
        print("\n" + "="*70)
        print("TEST CASE 1: Register Valid Candidate")
        print("="*70)
        
        data = {
            "firstName": "Rajesh",
            "lastName": "Kumar",
            "email": "rajesh.kumar@techmail.com",
            "role": "candidate",
            "password": "Secure@2024",
            "phone": "9876543210"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'message': 'User registered successfully', 'user_id': 'Rajesh210'}}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['message'] == 'User registered successfully'
        assert result['user_id'] == 'Rajesh210'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_02_register_valid_hr_with_company(self, client):
        """TC_REG_002: Register HR user with company name"""
        
        print("\n" + "="*70)
        print("TEST CASE 2: Register HR with Company Name")
        print("="*70)
        
        data = {
            "firstName": "Priya",
            "lastName": "Sharma",
            "companyName": "TechCorp Solutions",
            "email": "priya.hr@techcorp.in",
            "role": "hr",
            "password": "HRSecure#789",
            "phone": "8765432109"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'message': 'User registered successfully', 'user_id': 'Priya109'}}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['message'] == 'User registered successfully'
        assert result['user_id'] == 'Priya109'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_03_register_phone_with_special_chars(self, client):
        """TC_REG_003: Register with phone containing special characters"""
        
        print("\n" + "="*70)
        print("TEST CASE 3: Phone with Special Characters")
        print("="*70)
        
        data = {
            "firstName": "Vikram",
            "lastName": "Patel",
            "email": "vikram.p@jobseeker.net",
            "role": "candidate",
            "password": "Pass@1234",
            "phone": "+91-755-888-42-10"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should extract digits only -> 'Vikram210'")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Vikram210'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== NEGATIVE TEST CASES ====================
    
    def test_04_register_duplicate_email(self, client):
        """TC_REG_004: Register with duplicate email"""
        
        print("\n" + "="*70)
        print("TEST CASE 4: Duplicate Email")
        print("="*70)
        
        # First registration
        data1 = {
            "firstName": "Amit",
            "lastName": "Verma",
            "email": "amit.v@duplicate.test",
            "role": "candidate",
            "password": "Test@9876",
            "phone": "9123456789"
        }
        client.post('/api/auth/register', json=data1)
        
        # Try duplicate
        data2 = {
            "firstName": "Sneha",
            "lastName": "Reddy",
            "email": "amit.v@duplicate.test",  # Same email
            "role": "candidate",
            "password": "Different@456",
            "phone": "8234567890"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data2}")
        
        response = client.post('/api/auth/register', json=data2)
        result = response.get_json()
        
        print(f"Expected Status Code: 400")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Email already exists'}}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 400
        assert result['error'] == 'Email already exists'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_05_register_missing_phone(self, client):
        """TC_REG_005: Register without phone number"""
        
        print("\n" + "="*70)
        print("TEST CASE 5: Missing Phone Number")
        print("="*70)
        
        data = {
            "firstName": "Kavya",
            "lastName": "Nair",
            "email": "kavya.n@nophone.test",
            "role": "candidate",
            "password": "Secure#321"
            # phone is missing
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Phone number is required'}}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 400
        assert result['error'] == 'Phone number is required'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_06_register_empty_phone(self, client):
        """TC_REG_006: Register with empty phone string"""
        
        print("\n" + "="*70)
        print("TEST CASE 6: Empty Phone String")
        print("="*70)
        
        data = {
            "firstName": "Arjun",
            "lastName": "Singh",
            "email": "arjun.s@emptyphone.test",
            "role": "candidate",
            "password": "Pass@7890",
            "phone": ""  # Empty string
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: {{'error': 'Phone number is required'}}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 400
        assert result['error'] == 'Phone number is required'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_07_register_missing_firstName(self, client):
        """TC_REG_007: Register without firstName"""
        
        print("\n" + "="*70)
        print("TEST CASE 7: Missing firstName")
        print("="*70)
        
        data = {
            # firstName is missing
            "lastName": "Gupta",
            "email": "noname@missing.test",
            "role": "candidate",
            "password": "Test@4567",
            "phone": "7654321098"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400 or 500")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Actual Output: {result}")
        
        assert response.status_code in [400, 500]
        
        print("✅ TEST PASSED (Error handled)")
        print("="*70)
    
    def test_08_register_missing_email(self, client):
        """TC_REG_008: Register without email"""
        
        print("\n" + "="*70)
        print("TEST CASE 8: Missing Email")
        print("="*70)
        
        data = {
            "firstName": "Meera",
            "lastName": "Iyer",
            # email is missing
            "role": "candidate",
            "password": "Secure@654",
            "phone": "6543210987"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400 or 500")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Actual Output: {result}")
        
        assert response.status_code in [400, 500]
        
        print("✅ TEST PASSED (Error handled)")
        print("="*70)
    
    def test_09_register_missing_password(self, client):
        """TC_REG_009: Register without password"""
        
        print("\n" + "="*70)
        print("TEST CASE 9: Missing Password")
        print("="*70)
        
        data = {
            "firstName": "Rohan",
            "lastName": "Desai",
            "email": "rohan.d@nopass.test",
            "role": "candidate",
            # password is missing
            "phone": "5432109876"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400 or 500")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Actual Output: {result}")
        
        assert response.status_code in [400, 500]
        
        print("✅ TEST PASSED (Error handled)")
        print("="*70)
    
    # ==================== BOUNDARY TEST CASES ====================
    
    def test_10_register_phone_less_than_3_digits(self, client):
        """TC_REG_010: Phone with less than 3 digits"""
        
        print("\n" + "="*70)
        print("TEST CASE 10: Phone < 3 Digits (Boundary)")
        print("="*70)
        
        data = {
            "firstName": "Sanjay",
            "lastName": "Mehta",
            "email": "sanjay.m@shortphone.test",
            "role": "candidate",
            "password": "Bound@12",
            "phone": "45"  # Only 2 digits
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should be 'Sanjay45' (uses all available digits)")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Sanjay45'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_11_register_phone_exactly_3_digits(self, client):
        """TC_REG_011: Phone with exactly 3 digits"""
        
        print("\n" + "="*70)
        print("TEST CASE 11: Phone = 3 Digits (Boundary)")
        print("="*70)
        
        data = {
            "firstName": "Neha",
            "lastName": "Chopra",
            "email": "neha.c@exact3.test",
            "role": "candidate",
            "password": "Exact@789",
            "phone": "567"  # Exactly 3 digits
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should be 'Neha567'")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Neha567'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_12_register_phone_only_special_chars(self, client):
        """TC_REG_012: Phone with only special characters (no digits)"""
        
        print("\n" + "="*70)
        print("TEST CASE 12: Phone with No Digits (Edge Case)")
        print("="*70)
        
        data = {
            "firstName": "Kiran",
            "lastName": "Bhat",
            "email": "kiran.b@nodigits.test",
            "role": "candidate",
            "password": "Edge@321",
            "phone": "++--##"  # No digits
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should be 'Kiran' (no digits to append)")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Kiran'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_13_register_very_long_phone(self, client):
        """TC_REG_013: Phone with many digits"""
        
        print("\n" + "="*70)
        print("TEST CASE 13: Very Long Phone Number")
        print("="*70)
        
        data = {
            "firstName": "Aditya",
            "lastName": "Rao",
            "email": "aditya.r@longphone.test",
            "role": "candidate",
            "password": "Long@9876",
            "phone": "91234567890123456789"  # 20 digits
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should be 'Aditya789' (last 3 digits)")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Aditya789'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    # ==================== SPECIAL CHARACTER TEST CASES ====================
    
    def test_14_register_firstName_with_spaces(self, client):
        """TC_REG_014: firstName with spaces"""
        
        print("\n" + "="*70)
        print("TEST CASE 14: firstName with Spaces")
        print("="*70)
        
        data = {
            "firstName": "Ravi Kumar",
            "lastName": "Joshi",
            "email": "ravikumar.j@spaces.test",
            "role": "candidate",
            "password": "Space@456",
            "phone": "4321098765"
        }
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 201")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Output: user_id should be 'Ravi Kumar765'")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 201
        assert result['user_id'] == 'Ravi Kumar765'
        
        print("✅ TEST PASSED")
        print("="*70)
    
    def test_15_register_empty_json(self, client):
        """TC_REG_015: Empty JSON payload"""
        
        print("\n" + "="*70)
        print("TEST CASE 15: Empty JSON Payload")
        print("="*70)
        
        data = {}
        
        print(f"API Being Tested: POST /api/auth/register")
        print(f"Input: {data}")
        
        response = client.post('/api/auth/register', json=data)
        result = response.get_json()
        
        print(f"Expected Status Code: 400")
        print(f"Actual Status Code: {response.status_code}")
        print(f"Actual Output: {result}")
        
        assert response.status_code == 400
        
        print("✅ TEST PASSED (Error handled)")
        print("="*70)
