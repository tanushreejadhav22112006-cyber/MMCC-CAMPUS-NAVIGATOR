"""Test admin login flow"""
import requests
import json

# Test admin login
print("=" * 60)
print("Testing Admin Login Flow")
print("=" * 60)

# Test 1: Admin login endpoint
print("\n1. Testing admin login endpoint...")
response = requests.post(
    'http://127.0.0.1:5001/api/auth/admin/login',
    json={'email': 'admin@mmcc.edu', 'password': 'admin123'}
)

print(f"   Status: {response.status_code}")
data = response.json()
print(f"   Response: {json.dumps(data, indent=2)}")

if response.status_code == 200:
    print("\n   ✓ Admin login successful!")
    token = data['access_token']
    user_type = data['user']['user_type']
    print(f"   User Type: {user_type}")
    
    # Test 2: Access admin stats
    print("\n2. Testing admin stats endpoint...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    stats_response = requests.get(
        'http://127.0.0.1:5001/api/users/admin/stats',
        headers=headers
    )
    
    print(f"   Status: {stats_response.status_code}")
    if stats_response.status_code == 200:
        stats_data = stats_response.json()
        print(f"   ✓ Admin stats loaded successfully!")
        print(f"   Total Users: {stats_data.get('total_users', 0)}")
        print(f"   Total Logins: {stats_data.get('total_logins', 0)}")
        print(f"   Student Count: {stats_data.get('student_count', 0)}")
        print(f"   Faculty Count: {stats_data.get('faculty_count', 0)}")
        print(f"   Admin Count: {stats_data.get('admin_count', 0)}")
    else:
        print(f"   ✗ Failed to load admin stats")
        print(f"   Error: {stats_response.text}")
    
    # Test 3: Try regular login with admin credentials (should fail)
    print("\n3. Testing regular login with admin credentials (should be blocked)...")
    regular_response = requests.post(
        'http://127.0.0.1:5001/api/auth/login',
        json={'email': 'admin@mmcc.edu', 'password': 'admin123'}
    )
    
    print(f"   Status: {regular_response.status_code}")
    if regular_response.status_code != 200:
        regular_data = regular_response.json()
        print(f"   ✓ Admin blocked from regular login: {regular_data.get('error')}")
    else:
        print(f"   ✗ WARNING: Admin was able to login through regular endpoint!")
        
else:
    print(f"\n   ✗ Admin login failed!")
    print(f"   Error: {data.get('error')}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
