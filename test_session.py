#!/usr/bin/env python3
"""
Test script to verify session functionality
"""

import requests
import json

def test_signin_session():
    """Test sign-in and session functionality"""
    base_url = "http://localhost:5000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=== Testing Sign-In Session Functionality ===\n")
    
    # Test 1: Get sign-in page
    print("1. Getting sign-in page...")
    response = session.get(f"{base_url}/signin")
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print("❌ Failed to get sign-in page")
        return False
    
    print("✅ Sign-in page loaded successfully")
    
    # Test 2: Submit sign-in form
    print("\n2. Submitting sign-in form...")
    signin_data = {
        'email': 'demo@cyberstudy.com',
        'password': 'demo123',
        'rememberMe': 'on'
    }
    
    response = session.post(f"{base_url}/signin", data=signin_data)
    print(f"   Status: {response.status_code}")
    print(f"   URL after redirect: {response.url}")
    
    if response.status_code == 302 and 'parent-dashboard' in response.url:
        print("✅ Sign-in successful, redirected to dashboard")
    elif response.status_code == 200 and 'parent-dashboard' in response.url:
        print("✅ Sign-in successful, on dashboard page")
    else:
        print("❌ Sign-in failed or not redirected properly")
        print(f"   Response content preview: {response.text[:200]}...")
        return False
    
    # Test 3: Access dashboard data API
    print("\n3. Testing dashboard data API...")
    response = session.get(f"{base_url}/api/dashboard-data")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Dashboard data API accessible")
        data = response.json()
        print(f"   Parent name: {data.get('parent_name', 'N/A')}")
    else:
        print("❌ Dashboard data API not accessible")
        print(f"   Response: {response.text}")
        return False
    
    # Test 4: Access parent dashboard page
    print("\n4. Testing parent dashboard page...")
    response = session.get(f"{base_url}/parent-dashboard")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Parent dashboard page accessible")
    else:
        print("❌ Parent dashboard page not accessible")
        return False
    
    print("\n🎉 All tests passed! Session functionality is working correctly.")
    return True

if __name__ == "__main__":
    try:
        test_signin_session()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
