# import pytest
# import sys
# import os

# # Add parent directory to path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from app import create_app
# from app.database import db

# @pytest.fixture
# def client():
#     """Create test client"""
#     app = create_app()
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
#     with app.app_context():
#         db.create_all()
#         yield app.test_client()
#         db.drop_all()


# def test_register_success(client):
#     """Test Case: Register with valid data"""
    
#     # Input data
#     data = {
#         'firstName': 'John',
#         'lastName': 'Doe',
#         'email': 'john@example.com',
#         'phone': '9876543210',
#         'password': 'Pass123!',
#         'role': 'applicant'
#     }
    
#     # Make request
#     response = client.post('/auth/register', json=data)
    
#     # Print results
#     print("\n" + "="*50)
#     print("TEST: Register User")
#     print("="*50)
#     print(f"Input: {data}")
#     print(f"Expected Status: 201")
#     print(f"Actual Status: {response.status_code}")
#     print(f"Response: {response.get_json()}")
#     print("="*50)
    
#     # Check result
#     assert response.status_code == 201
#     result = response.get_json()
#     assert result['message'] == 'User registered successfully'
#     assert result['user_id'] == 'John210'
    
#     print("✅ TEST PASSED")
