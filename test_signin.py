#!/usr/bin/env python3
"""
Test script to verify sign-in functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_demo_user, load_users, verify_password, hash_password

def test_demo_user_creation():
    """Test if demo user is created correctly"""
    print("Testing demo user creation...")
    
    # Create demo user
    create_demo_user()
    
    # Load users and check if demo user exists
    users = load_users()
    print(f"Total users in database: {len(users)}")
    
    demo_user = None
    for user in users:
        if user['email'] == 'demo@cyberstudy.com':
            demo_user = user
            break
    
    if demo_user:
        print("✅ Demo user found in database")
        print(f"   User ID: {demo_user['id']}")
        print(f"   Email: {demo_user['email']}")
        print(f"   Parent Name: {demo_user['parent_name']}")
        
        # Test password verification
        test_password = 'demo123'
        if verify_password(test_password, demo_user['password_hash'], demo_user['salt']):
            print("✅ Password verification works correctly")
        else:
            print("❌ Password verification failed")
            
    else:
        print("❌ Demo user not found in database")
        return False
    
    return True

def test_password_hashing():
    """Test password hashing functionality"""
    print("\nTesting password hashing...")
    
    test_password = 'test123'
    password_hash, salt = hash_password(test_password)
    
    print(f"   Original password: {test_password}")
    print(f"   Generated hash: {password_hash[:20]}...")
    print(f"   Generated salt: {salt[:20]}...")
    
    # Test verification
    if verify_password(test_password, password_hash, salt):
        print("✅ Password hashing and verification works correctly")
        return True
    else:
        print("❌ Password hashing verification failed")
        return False

if __name__ == "__main__":
    print("=== Sign-In Functionality Test ===\n")
    
    # Test password hashing
    hash_test = test_password_hashing()
    
    # Test demo user creation
    user_test = test_demo_user_creation()
    
    print(f"\n=== Test Results ===")
    print(f"Password Hashing: {'✅ PASS' if hash_test else '❌ FAIL'}")
    print(f"Demo User Creation: {'✅ PASS' if user_test else '❌ FAIL'}")
    
    if hash_test and user_test:
        print("\n🎉 All tests passed! Sign-in functionality should work correctly.")
        print("\nDemo credentials:")
        print("   Email: demo@cyberstudy.com")
        print("   Password: demo123")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
