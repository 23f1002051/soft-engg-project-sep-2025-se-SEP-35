import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_auth_ping(client):
    """Test Case: Auth Ping Endpoint"""
    
    print("\n" + "="*60)
    print("TEST CASE: Auth Ping")
    print("="*60)
    
    # Make GET request to /api/auth/ping
    response = client.get('/api/auth/ping')
    
    # Get response data
    data = response.get_json()
    
    # Print test details
    print(f"API Being Tested: GET /api/auth/ping")
    print(f"Input: None (GET request)")
    print(f"Expected Status Code: 200")
    print(f"Actual Status Code: {response.status_code}")
    print(f"Expected Output: {{'msg': 'auth ok'}}")
    print(f"Actual Output: {data}")
    
    # Assertions
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert data is not None, "Response data is None"
    assert 'msg' in data, "Response missing 'msg' key"
    assert data['msg'] == 'auth ok', f"Expected 'auth ok', got '{data['msg']}'"
    
    print("\n✅ TEST PASSED")
    print("="*60)
